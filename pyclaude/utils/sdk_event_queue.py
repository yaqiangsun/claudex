"""
SDK event queue utilities.

SDK event queue handling.
"""

import asyncio
from typing import Any, List


class SdkEventQueue:
    """SDK event queue."""

    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()

    async def put(self, event: Any) -> None:
        """Add event to queue."""
        await self._queue.put(event)

    async def get(self) -> Any:
        """Get event from queue."""
        return await self._queue.get()


_queue = SdkEventQueue()


def get_sdk_event_queue() -> SdkEventQueue:
    """Get global SDK event queue."""
    return _queue


__all__ = [
    "SdkEventQueue",
    "get_sdk_event_queue",
]