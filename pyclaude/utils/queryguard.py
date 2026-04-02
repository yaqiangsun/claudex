"""
Query guard utility.

Synchronous state machine for the query lifecycle.
"""

from typing import Optional, Callable, List


class QueryGuard:
    """State machine for query lifecycle management."""

    def __init__(self):
        self._status: str = 'idle'  # 'idle' | 'dispatching' | 'running'
        self._generation: int = 0
        self._subscribers: List[Callable[[], None]] = []

    def reserve(self) -> bool:
        """Reserve the guard for queue processing."""
        if self._status != 'idle':
            return False
        self._status = 'dispatching'
        self._notify()
        return True

    def cancel_reservation(self) -> None:
        """Cancel a reservation."""
        if self._status != 'dispatching':
            return
        self._status = 'idle'
        self._notify()

    def try_start(self) -> Optional[int]:
        """Start a query. Returns generation number on success."""
        if self._status == 'running':
            return None
        self._status = 'running'
        self._generation += 1
        self._notify()
        return self._generation

    def end(self, generation: int) -> bool:
        """End a query. Returns true if this generation is current."""
        if self._generation != generation:
            return False
        if self._status != 'running':
            return False
        self._status = 'idle'
        self._notify()
        return True

    def force_end(self) -> None:
        """Force-end the current query."""
        if self._status == 'idle':
            return
        self._status = 'idle'
        self._generation += 1
        self._notify()

    @property
    def is_active(self) -> bool:
        """Is the guard active (dispatching or running)?"""
        return self._status != 'idle'

    @property
    def generation(self) -> int:
        """Current generation number."""
        return self._generation

    def subscribe(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Subscribe to state changes."""
        self._subscribers.append(callback)
        return lambda: self._subscribers.remove(callback)

    def get_snapshot(self) -> bool:
        """Get snapshot for useSyncExternalStore."""
        return self._status != 'idle'

    def _notify(self) -> None:
        """Notify subscribers of state change."""
        for callback in self._subscribers:
            callback()


__all__ = ['QueryGuard']