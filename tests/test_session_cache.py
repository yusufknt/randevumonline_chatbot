from __future__ import annotations

import asyncio
import unittest
from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, patch

from app.channels.whatsapp.flow import _cached_available_slots
from app.core.session_cache import get_booking_session_cache
from app.core.session_cache import HybridVoiceSessionCache, SessionTTLCache
from app.voice.dialog import DialogManager
from app.voice.message_buffer import ConversationMessageBuffer


class _FakePipeline:
    def __init__(self, redis) -> None:
        self.redis = redis
        self.commands = []

    def hset(self, key, field, value):
        self.commands.append(("hset", key, field, value))
        return self

    def expire(self, key, ttl):
        self.commands.append(("expire", key, ttl))
        return self

    async def execute(self):
        for command in self.commands:
            if command[0] == "hset":
                _, key, field, value = command
                self.redis.values.setdefault(key, {})[field] = value
        return [True] * len(self.commands)


class _FakeRedis:
    def __init__(self, *, failing: bool = False) -> None:
        self.values = {}
        self.failing = failing

    async def hget(self, key, field):
        if self.failing:
            raise ConnectionError("redis unavailable")
        return self.values.get(key, {}).get(field)

    def pipeline(self, transaction=False):
        if self.failing:
            raise ConnectionError("redis unavailable")
        return _FakePipeline(self)

    async def delete(self, key):
        self.values.pop(key, None)

    async def ping(self):
        if self.failing:
            raise ConnectionError("redis unavailable")
        return True

    async def aclose(self):
        return None


class _FakeCursor:
    def __init__(self, values) -> None:
        self.values = values

    async def to_list(self, _limit):
        return list(self.values)


class _FakeCollection:
    def __init__(self, values) -> None:
        self.values = values
        self.find_calls = 0

    def find(self, _query):
        self.find_calls += 1
        return _FakeCursor(self.values)


class SessionTTLCacheTests(unittest.IsolatedAsyncioTestCase):
    async def test_reuses_value_inside_same_session(self) -> None:
        cache = SessionTTLCache(ttl_seconds=60)
        calls = 0

        async def load() -> list[str]:
            nonlocal calls
            calls += 1
            return ["10:00", "10:30"]

        first = await cache.get_or_load("session-a", ("slots", "day"), load)
        second = await cache.get_or_load("session-a", ("slots", "day"), load)

        self.assertIs(first, second)
        self.assertEqual(calls, 1)

    async def test_sessions_are_isolated(self) -> None:
        cache = SessionTTLCache(ttl_seconds=60)
        calls = 0

        async def load() -> int:
            nonlocal calls
            calls += 1
            return calls

        first = await cache.get_or_load("session-a", "staff", load)
        second = await cache.get_or_load("session-b", "staff", load)

        self.assertEqual((first, second), (1, 2))

    async def test_concurrent_loads_are_coalesced(self) -> None:
        cache = SessionTTLCache(ttl_seconds=60)
        calls = 0

        async def load() -> str:
            nonlocal calls
            calls += 1
            await asyncio.sleep(0)
            return "Mehmet"

        values = await asyncio.gather(*(
            cache.get_or_load("session", "staff", load) for _ in range(10)
        ))

        self.assertEqual(values, ["Mehmet"] * 10)
        self.assertEqual(calls, 1)

    async def test_clear_session_forces_fresh_load(self) -> None:
        cache = SessionTTLCache(ttl_seconds=60)
        calls = 0

        async def load() -> int:
            nonlocal calls
            calls += 1
            return calls

        await cache.get_or_load("session", "slots", load)
        cache.clear_session("session")
        value = await cache.get_or_load("session", "slots", load)

        self.assertEqual(value, 2)
        self.assertEqual(calls, 2)

    async def test_whatsapp_day_and_time_steps_share_slot_query(self) -> None:
        session_id = "whatsapp-flow:test-cache"
        slots = [datetime(2026, 7, 22, 10, tzinfo=timezone.utc)]
        business = {"_id": "business"}
        service = {"_id": "service"}
        staff = {"_id": "staff"}
        cache = get_booking_session_cache()
        cache.clear_session(session_id)

        with patch(
            "app.channels.whatsapp.flow.compute_available_slots",
            AsyncMock(return_value=slots),
        ) as query:
            day_slots = await _cached_available_slots(
                object(), business, service, staff, date(2026, 7, 22), 30, session_id
            )
            time_slots = await _cached_available_slots(
                object(), business, service, staff, date(2026, 7, 22), 30, session_id
            )

        cache.clear_session(session_id)
        self.assertEqual(day_slots, time_slots)
        query.assert_awaited_once()

    async def test_hybrid_cache_reuses_l1_and_single_flights_loader(self) -> None:
        redis = _FakeRedis()
        cache = HybridVoiceSessionCache(redis_url="", redis_client=redis)
        loader = AsyncMock(return_value=["10:00"])

        values = await asyncio.gather(*(
            cache.get_or_load(
                "voice:call", ("slots", "day"), loader, kind="availability"
            )
            for _ in range(8)
        ))

        self.assertEqual(values, [["10:00"]] * 8)
        loader.assert_awaited_once()
        await cache.close()

    async def test_hybrid_cache_uses_redis_between_cache_instances(self) -> None:
        redis = _FakeRedis()
        first = HybridVoiceSessionCache(redis_url="", redis_client=redis)
        second = HybridVoiceSessionCache(redis_url="", redis_client=redis)
        loader = AsyncMock(return_value=["Mehmet"])

        loaded = await first.get_or_load("voice:call", "staff", loader)
        reused = await second.get_or_load("voice:call", "staff", loader)

        self.assertEqual(loaded, reused)
        loader.assert_awaited_once()
        await first.close()
        await second.close()

    async def test_hybrid_cache_falls_back_when_redis_is_down(self) -> None:
        cache = HybridVoiceSessionCache(
            redis_url="", redis_client=_FakeRedis(failing=True)
        )
        loader = AsyncMock(return_value=["Yusuf"])

        first = await cache.get_or_load("voice:call", "staff", loader)
        second = await cache.get_or_load("voice:call", "staff", loader)

        self.assertEqual(first, second)
        loader.assert_awaited_once()
        await cache.close()

    async def test_hybrid_clear_isolated_session_and_forces_reload(self) -> None:
        cache = HybridVoiceSessionCache(
            redis_url="", redis_client=_FakeRedis()
        )
        loader = AsyncMock(side_effect=[["first"], ["second"]])
        await cache.get_or_load("voice:a", "staff", loader)
        await cache.clear_session_wait("voice:a")

        value = await cache.get_or_load("voice:a", "staff", loader)

        self.assertEqual(value, ["second"])
        self.assertEqual(loader.await_count, 2)
        await cache.close()

    async def test_message_buffer_preserves_order_and_batches_writes(self) -> None:
        with patch(
            "app.voice.message_buffer.append_conversation_messages",
            AsyncMock(),
        ) as writer:
            buffer = ConversationMessageBuffer("conversation", flush_interval_s=.05)
            buffer.enqueue({"role": "user", "content": "Mehmet"})
            buffer.enqueue({"role": "assistant", "content": "Hangi gün?"})
            buffer.enqueue({"role": "user", "content": "Yarın"})
            await buffer.close()

        writer.assert_awaited_once()
        written = writer.await_args.args[1]
        self.assertEqual(
            [item["content"] for item in written],
            ["Mehmet", "Hangi gün?", "Yarın"],
        )

    async def test_voice_catalog_is_loaded_once_and_reused_from_cache(self) -> None:
        redis = _FakeRedis()
        cache = HybridVoiceSessionCache(redis_url="", redis_client=redis)
        db = type("FakeDb", (), {})()
        db.services = _FakeCollection([{"_id": "s", "name": "Saç Kesimi"}])
        db.staff = _FakeCollection([{"_id": "m", "name": "Mehmet Kaya"}])
        first = DialogManager({"_id": "business"}, "+90500", "call-a")
        second = DialogManager({"_id": "business"}, "+90501", "call-b")
        first._cache = second._cache = cache

        with (
            patch("app.voice.dialog.get_db", return_value=db),
            patch(
                "app.voice.dialog.upsert_customer_by_phone",
                AsyncMock(return_value={"_id": "customer"}),
            ),
            patch(
                "app.voice.dialog.upsert_conversation",
                AsyncMock(return_value={"_id": "conversation"}),
            ),
        ):
            await first.initialize()
            await second.initialize()

        self.assertEqual(db.services.find_calls, 1)
        self.assertEqual(db.staff.find_calls, 1)
        self.assertEqual(first.services, second.services)
        self.assertEqual(first.staff, second.staff)
        await first.shutdown()
        await second.shutdown()
        await cache.close()
