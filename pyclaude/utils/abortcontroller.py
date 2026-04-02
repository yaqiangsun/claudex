"""
Abort controller utility.

Abort controller polyfill for Python.
"""

import threading
from typing import Optional, Callable


class AbortController:
    """Abort controller implementation."""

    def __init__(self):
        self._signal: Optional[AbortSignal] = None
        self._aborted = False
        self._lock = threading.Lock()

    @property
    def signal(self) -> 'AbortSignal':
        """Get the abort signal."""
        if self._signal is None:
            self._signal = AbortSignal(self)
        return self._signal

    def abort(self) -> None:
        """Abort the operation."""
        with self._lock:
            self._aborted = True
            if self._signal:
                self._signal._notify()


class AbortSignal:
    """Abort signal implementation."""

    def __init__(self, controller: AbortController):
        self._controller = controller
        self._aborted = False
        self._reason: Optional[Exception] = None
        self._listeners: list = []

    @property
    def aborted(self) -> bool:
        """Check if aborted."""
        with self._controller._lock:
            return self._controller._aborted

    def add_event_listener(self, callback: Callable) -> None:
        """Add an abort listener."""
        self._listeners.append(callback)

    def remove_event_listener(self, callback: Callable) -> None:
        """Remove an abort listener."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def _notify(self) -> None:
        """Notify all listeners."""
        self._aborted = True
        for callback in self._listeners:
            callback(self)


__all__ = ['AbortController', 'AbortSignal']