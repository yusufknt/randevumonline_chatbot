from __future__ import annotations

import asyncio
import logging
from typing import Any

from bson import ObjectId
from prometheus_client import Counter, Histogram

from app.core.db import append_conversation_messages


log = logging.getLogger(__name__)

MESSAGE_FLUSHES = Counter(
    "voice_message_flush_total",
    "Arka plan konuşma mesajı yazma sonuçları",
    ("result",),
)
MESSAGE_BATCH_SIZE = Histogram(
    "voice_message_flush_batch_size",
    "Tek MongoDB yazımındaki konuşma mesajı sayısı",
    buckets=(1, 2, 4, 8),
)


class ConversationMessageBuffer:
    """Mesajları cevap yolunu bekletmeden sıralı MongoDB gruplarına çevirir."""

    _STOP = object()

    def __init__(
        self,
        conversation_id: ObjectId,
        *,
        flush_interval_s: float = .05,
        batch_size: int = 8,
    ) -> None:
        self.conversation_id = conversation_id
        self.flush_interval_s = flush_interval_s
        self.batch_size = batch_size
        self._queue: asyncio.Queue[dict | object] = asyncio.Queue()
        self._task: asyncio.Task[None] | None = None
        self._closing = False

    def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._run())

    def enqueue(self, message: dict) -> None:
        if self._closing:
            log.warning("Kapanan mesaj tamponuna yeni kayıt alınmadı")
            return
        self.start()
        self._queue.put_nowait(message)

    async def _write_batch(self, batch: list[dict]) -> None:
        retry_delays = (.1, .25, .5)
        for attempt in range(len(retry_delays) + 1):
            try:
                await append_conversation_messages(self.conversation_id, batch)
                MESSAGE_FLUSHES.labels("success").inc()
                MESSAGE_BATCH_SIZE.observe(len(batch))
                return
            except Exception as exc:
                if attempt == len(retry_delays):
                    MESSAGE_FLUSHES.labels("failed").inc()
                    log.error(
                        "Konuşma mesaj grubu yazılamadı count=%d type=%s",
                        len(batch),
                        type(exc).__name__,
                    )
                    return
                MESSAGE_FLUSHES.labels("retry").inc()
                await asyncio.sleep(retry_delays[attempt])

    async def _run(self) -> None:
        stopping = False
        while not stopping:
            first = await self._queue.get()
            if first is self._STOP:
                break
            batch: list[dict[str, Any]] = [first]  # type: ignore[list-item]
            deadline = asyncio.get_running_loop().time() + self.flush_interval_s
            while len(batch) < self.batch_size:
                remaining = deadline - asyncio.get_running_loop().time()
                if remaining <= 0:
                    break
                try:
                    item = await asyncio.wait_for(
                        self._queue.get(), timeout=remaining
                    )
                except asyncio.TimeoutError:
                    break
                if item is self._STOP:
                    stopping = True
                    break
                batch.append(item)  # type: ignore[arg-type]
            await self._write_batch(batch)

    async def close(self, timeout_s: float = 2.0) -> None:
        if self._task is None:
            return
        if not self._closing:
            self._closing = True
            self._queue.put_nowait(self._STOP)
        try:
            await asyncio.wait_for(asyncio.shield(self._task), timeout=timeout_s)
        except asyncio.TimeoutError:
            MESSAGE_FLUSHES.labels("close_timeout").inc()
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        finally:
            self._task = None
