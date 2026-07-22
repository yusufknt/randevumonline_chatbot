from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Awaitable, Callable, Hashable, TypeVar

from bson import BSON
from prometheus_client import Counter, Histogram

try:
    from redis.asyncio import Redis
except ImportError:  # Redis opsiyonel hızlandırma katmanıdır.
    Redis = None  # type: ignore[assignment,misc]

from app.core.config import get_settings


T = TypeVar("T")
CacheKey = Hashable
log = logging.getLogger(__name__)

CACHE_REQUESTS = Counter(
    "voice_cache_requests_total",
    "Sesli rezervasyon cache istekleri",
    ("layer", "result", "kind"),
)
CACHE_LOAD_SECONDS = Histogram(
    "voice_cache_loader_seconds",
    "Cache miss sonrasında MongoDB loader süresi",
    ("kind",),
    buckets=(.005, .01, .025, .05, .1, .25, .5, 1, 2),
)


@dataclass(slots=True)
class _Entry:
    value: object
    expires_at: float


class SessionTTLCache:
    """Process içi, oturum bazlı, sınırlı ve TTL'li async cache.

    Her API/voice process'i kendi cache'ini taşır. Aynı oturumdaki eşzamanlı aynı
    anahtar yüklemeleri tek loader çağrısında birleştirilir (single-flight).
    """

    def __init__(
        self,
        ttl_seconds: float = 120.0,
        max_sessions: int = 2_000,
        max_entries_per_session: int = 256,
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds pozitif olmalı")
        if max_sessions <= 0 or max_entries_per_session <= 0:
            raise ValueError("cache sınırları pozitif olmalı")
        self.ttl_seconds = ttl_seconds
        self.max_sessions = max_sessions
        self.max_entries_per_session = max_entries_per_session
        self._sessions: OrderedDict[
            str, OrderedDict[CacheKey, _Entry]
        ] = OrderedDict()
        self._locks: dict[tuple[str, CacheKey], asyncio.Lock] = {}

    def _get(self, session_id: str, key: CacheKey) -> tuple[bool, object | None]:
        bucket = self._sessions.get(session_id)
        if bucket is None:
            return False, None
        entry = bucket.get(key)
        if entry is None:
            return False, None
        if entry.expires_at <= time.monotonic():
            del bucket[key]
            if not bucket:
                del self._sessions[session_id]
            return False, None
        bucket.move_to_end(key)
        self._sessions.move_to_end(session_id)
        return True, entry.value

    def set(
        self,
        session_id: str,
        key: CacheKey,
        value: object,
        *,
        ttl_seconds: float | None = None,
    ) -> None:
        bucket = self._sessions.setdefault(session_id, OrderedDict())
        ttl = self.ttl_seconds if ttl_seconds is None else ttl_seconds
        bucket[key] = _Entry(value, time.monotonic() + ttl)
        bucket.move_to_end(key)
        while len(bucket) > self.max_entries_per_session:
            evicted_key, _ = bucket.popitem(last=False)
            self._locks.pop((session_id, evicted_key), None)
        self._sessions.move_to_end(session_id)
        while len(self._sessions) > self.max_sessions:
            evicted_session, _ = self._sessions.popitem(last=False)
            for lock_key in tuple(self._locks):
                if lock_key[0] == evicted_session:
                    self._locks.pop(lock_key, None)

    async def get_or_load(
        self,
        session_id: str,
        key: CacheKey,
        loader: Callable[[], Awaitable[T]],
    ) -> T:
        hit, value = self._get(session_id, key)
        if hit:
            return value  # type: ignore[return-value]

        lock_key = (session_id, key)
        lock = self._locks.setdefault(lock_key, asyncio.Lock())
        async with lock:
            hit, value = self._get(session_id, key)
            if hit:
                return value  # type: ignore[return-value]
            loaded = await loader()
            self.set(session_id, key, loaded)
            return loaded

    def clear_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        for lock_key in tuple(self._locks):
            if lock_key[0] == session_id:
                self._locks.pop(lock_key, None)


@lru_cache
def get_booking_session_cache() -> SessionTTLCache:
    settings = get_settings()
    return SessionTTLCache(
        ttl_seconds=settings.booking_session_cache_ttl_s,
        max_sessions=settings.booking_session_cache_max_sessions,
        max_entries_per_session=settings.booking_session_cache_max_entries,
    )


class HybridVoiceSessionCache:
    """Sesli çağrılar için process belleği + Redis cache.

    Redis hiçbir zaman doğruluk kaynağı değildir. Bağlantı kurulamazsa çağrı L1
    cache ve loader (MongoDB) ile kesintisiz devam eder.
    """

    def __init__(
        self,
        *,
        redis_url: str,
        session_ttl_seconds: float = 600.0,
        catalog_ttl_seconds: float = 60.0,
        timeout_seconds: float = .1,
        max_sessions: int = 2_000,
        max_entries_per_session: int = 256,
        redis_client: Any | None = None,
    ) -> None:
        self.session_ttl_seconds = session_ttl_seconds
        self.catalog_ttl_seconds = catalog_ttl_seconds
        self._local = SessionTTLCache(
            ttl_seconds=session_ttl_seconds,
            max_sessions=max_sessions,
            max_entries_per_session=max_entries_per_session,
        )
        self._locks: dict[tuple[str, CacheKey], asyncio.Lock] = {}
        self._cleanup_tasks: set[asyncio.Task[Any]] = set()
        if redis_client is not None:
            self._redis = redis_client
        elif Redis is not None and redis_url:
            self._redis = Redis.from_url(
                redis_url,
                decode_responses=False,
                socket_connect_timeout=timeout_seconds,
                socket_timeout=timeout_seconds,
                retry_on_timeout=False,
            )
        else:
            self._redis = None

    @staticmethod
    def _redis_key(session_id: str) -> str:
        digest = hashlib.sha256(session_id.encode()).hexdigest()
        return f"randevumonline:voice-cache:{digest}"

    @staticmethod
    def _redis_field(key: CacheKey) -> str:
        raw = json.dumps(key, ensure_ascii=False, default=str, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def _ttl_for(self, session_id: str) -> float:
        return (
            self.catalog_ttl_seconds
            if session_id.startswith("voice-catalog:")
            else self.session_ttl_seconds
        )

    async def _redis_get(
        self, session_id: str, key: CacheKey, kind: str
    ) -> object | None:
        if self._redis is None:
            return None
        try:
            raw = await self._redis.hget(
                self._redis_key(session_id), self._redis_field(key)
            )
            if raw is None:
                CACHE_REQUESTS.labels("redis", "miss", kind).inc()
                return None
            value = BSON(raw).decode()["value"]
            CACHE_REQUESTS.labels("redis", "hit", kind).inc()
            return value
        except Exception as exc:
            CACHE_REQUESTS.labels("redis", "error", kind).inc()
            log.warning("Redis cache okuma başarısız type=%s", type(exc).__name__)
            return None

    async def _redis_set(
        self,
        session_id: str,
        key: CacheKey,
        value: object,
        ttl_seconds: float,
        kind: str,
    ) -> None:
        if self._redis is None:
            return
        redis_key = self._redis_key(session_id)
        try:
            payload = BSON.encode({"value": value})
            pipe = self._redis.pipeline(transaction=False)
            pipe.hset(redis_key, self._redis_field(key), payload)
            pipe.expire(redis_key, max(1, round(ttl_seconds)))
            await pipe.execute()
            CACHE_REQUESTS.labels("redis", "set", kind).inc()
        except Exception as exc:
            CACHE_REQUESTS.labels("redis", "error", kind).inc()
            log.warning("Redis cache yazma başarısız type=%s", type(exc).__name__)

    async def get_or_load(
        self,
        session_id: str,
        key: CacheKey,
        loader: Callable[[], Awaitable[T]],
        *,
        kind: str = "entry",
        ttl_seconds: float | None = None,
    ) -> T:
        ttl = self._ttl_for(session_id) if ttl_seconds is None else ttl_seconds
        hit, value = self._local._get(session_id, key)
        if hit:
            CACHE_REQUESTS.labels("memory", "hit", kind).inc()
            return value  # type: ignore[return-value]
        CACHE_REQUESTS.labels("memory", "miss", kind).inc()

        lock_key = (session_id, key)
        lock = self._locks.setdefault(lock_key, asyncio.Lock())
        async with lock:
            hit, value = self._local._get(session_id, key)
            if hit:
                CACHE_REQUESTS.labels("memory", "hit", kind).inc()
                return value  # type: ignore[return-value]

            value = await self._redis_get(session_id, key, kind)
            if value is not None:
                self._local.set(
                    session_id, key, value, ttl_seconds=ttl
                )
                return value  # type: ignore[return-value]

            started = time.monotonic()
            loaded = await loader()
            CACHE_LOAD_SECONDS.labels(kind).observe(time.monotonic() - started)
            CACHE_REQUESTS.labels("loader", "load", kind).inc()
            self._local.set(session_id, key, loaded, ttl_seconds=ttl)
            await self._redis_set(session_id, key, loaded, ttl, kind)
            return loaded

    async def ping(self) -> bool:
        if self._redis is None:
            return False
        try:
            return bool(await self._redis.ping())
        except Exception:
            return False

    async def _delete_redis_session(self, session_id: str) -> None:
        if self._redis is None:
            return
        try:
            await self._redis.delete(self._redis_key(session_id))
        except Exception as exc:
            log.warning("Redis oturum temizleme başarısız type=%s", type(exc).__name__)

    def clear_session(self, session_id: str) -> None:
        """Kritik yolda L1'i hemen, Redis'i arka planda temizle."""
        self._local.clear_session(session_id)
        for lock_key in tuple(self._locks):
            if lock_key[0] == session_id:
                self._locks.pop(lock_key, None)
        if self._redis is None:
            return
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        task = loop.create_task(self._delete_redis_session(session_id))
        self._cleanup_tasks.add(task)
        task.add_done_callback(self._cleanup_tasks.discard)

    async def clear_session_wait(self, session_id: str) -> None:
        self._local.clear_session(session_id)
        for lock_key in tuple(self._locks):
            if lock_key[0] == session_id:
                self._locks.pop(lock_key, None)
        await self._delete_redis_session(session_id)

    async def close(self) -> None:
        if self._cleanup_tasks:
            await asyncio.gather(*tuple(self._cleanup_tasks), return_exceptions=True)
        if self._redis is not None:
            await self._redis.aclose()


@lru_cache
def get_voice_session_cache() -> HybridVoiceSessionCache:
    settings = get_settings()
    return HybridVoiceSessionCache(
        redis_url=settings.redis_url,
        session_ttl_seconds=settings.voice_cache_session_ttl_s,
        catalog_ttl_seconds=settings.voice_cache_catalog_ttl_s,
        timeout_seconds=settings.voice_cache_redis_timeout_s,
        max_sessions=settings.booking_session_cache_max_sessions,
        max_entries_per_session=settings.booking_session_cache_max_entries,
    )


async def close_voice_session_cache() -> None:
    cache = get_voice_session_cache()
    await cache.close()
    get_voice_session_cache.cache_clear()
