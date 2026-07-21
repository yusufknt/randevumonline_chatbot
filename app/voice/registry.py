from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field


@dataclass(slots=True)
class CallContext:
    uuid: str
    caller: str
    did: str
    asterisk_uniqueid: str
    created_monotonic: float = field(default_factory=time.monotonic)


class CallRegistry:
    def __init__(self) -> None:
        self._calls: dict[str, CallContext] = {}
        self._condition = asyncio.Condition()

    async def put(self, context: CallContext) -> None:
        async with self._condition:
            self._calls[context.uuid] = context
            self._condition.notify_all()

    async def wait(self, call_uuid: str, timeout: float = 3.0) -> CallContext | None:
        async with self._condition:
            if call_uuid not in self._calls:
                try:
                    await asyncio.wait_for(
                        self._condition.wait_for(lambda: call_uuid in self._calls),
                        timeout,
                    )
                except TimeoutError:
                    return None
            return self._calls.get(call_uuid)

    async def remove(self, call_uuid: str) -> None:
        async with self._condition:
            self._calls.pop(call_uuid, None)

    def count(self) -> int:
        return len(self._calls)


registry = CallRegistry()
