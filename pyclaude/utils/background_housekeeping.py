"""
Background housekeeping utilities.

Background cleanup tasks.
"""

import asyncio
from typing import Callable, Optional, List, Any


class BackgroundHousekeeping:
    """Background housekeeping tasks."""

    def __init__(self):
        self._tasks: List[asyncio.Task] = []
        self._running = False

    async def schedule(self, func: Callable, interval_seconds: int) -> None:
        """Schedule a background task."""
        async def run():
            while self._running:
                try:
                    await func()
                except Exception:
                    pass
                await asyncio.sleep(interval_seconds)

        task = asyncio.create_task(run())
        self._tasks.append(task)

    async def start(self) -> None:
        """Start housekeeping."""
        self._running = True

    async def stop(self) -> None:
        """Stop housekeeping."""
        self._running = False
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()


_housekeeping = BackgroundHousekeeping()


def get_housekeeping() -> BackgroundHousekeeping:
    """Get global housekeeping instance."""
    return _housekeeping


__all__ = [
    "BackgroundHousekeeping",
    "get_housekeeping",
]