"""
Use elapsed time hook - returns formatted elapsed time since startTime.

Python adaptation using observer pattern.
"""

from typing import Callable, Optional
import time
import threading


def format_duration(ms: int) -> str:
    """Format milliseconds to duration string (e.g., '1m 23s')."""
    if ms < 0:
        ms = 0
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60

    if hours > 0:
        return f"{hours}h {minutes % 60}m"
    if minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    if seconds > 0:
        return f"{seconds}s"
    return f"{ms}ms"


class ElapsedTimeState:
    """State for elapsed time tracking."""

    def __init__(
        self,
        start_time: float,
        is_running: bool,
        update_interval_ms: float = 1000,
        paused_ms: float = 0,
        end_time: Optional[float] = None,
    ):
        self.start_time = start_time
        self.is_running = is_running
        self.update_interval_ms = update_interval_ms
        self.paused_ms = paused_ms
        self.end_time = end_time
        self._timer: Optional[threading.Timer] = None
        self._subscribers: list[Callable] = []
        self._last_value: str = ""

    def get(self) -> str:
        """Get formatted elapsed time."""
        end = self.end_time if self.end_time is not None else time.time() * 1000
        elapsed = max(0, end - self.start_time - self.paused_ms)
        self._last_value = format_duration(int(elapsed))
        return self._last_value

    def subscribe(self, callback: Callable) -> Callable:
        """Subscribe to updates. Returns unsubscribe function."""
        self._subscribers.append(callback)

        if self.is_running and self._timer is None:
            self._start_timer()

        def unsubscribe():
            self._subscribers.remove(callback)
            if not self._subscribers and self._timer:
                self._timer.cancel()
                self._timer = None

        return unsubscribe

    def _start_timer(self):
        """Start the update timer."""
        self._timer = threading.Timer(
            self.update_interval_ms / 1000,
            self._notify_and_reschedule,
        )
        self._timer.daemon = True
        self._timer.start()

    def _notify_and_reschedule(self):
        """Notify subscribers and reschedule."""
        for callback in self._subscribers:
            callback()
        self._timer = None
        if self._subscribers and self.is_running:
            self._start_timer()


# Global state storage
_elapsed_time_states: dict[int, ElapsedTimeState] = {}


def use_elapsed_time(
    start_time_ms: float,
    is_running: bool,
    update_interval_ms: float = 1000,
    paused_ms: float = 0,
    end_time_ms: Optional[float] = None,
) -> str:
    """Hook that returns formatted elapsed time since startTime.

    Args:
        start_time_ms: Unix timestamp in milliseconds
        is_running: Whether to actively update the timer
        update_interval_ms: How often to trigger updates (default 1000ms)
        paused_ms: Total paused duration to subtract
        end_time_ms: If set, freezes the duration at this timestamp

    Returns:
        Formatted duration string (e.g., '1m 23s')
    """
    # Use id-based key for simplicity in Python
    key = id(use_elapsed_time)

    if key not in _elapsed_time_states:
        _elapsed_time_states[key] = ElapsedTimeState(
            start_time=start_time_ms,
            is_running=is_running,
            update_interval_ms=update_interval_ms,
            paused_ms=paused_ms,
            end_time=end_time_ms,
        )

    state = _elapsed_time_states[key]
    # Update parameters
    state.start_time = start_time_ms
    state.is_running = is_running
    state.update_interval_ms = update_interval_ms
    state.paused_ms = paused_ms
    state.end_time = end_time_ms

    return state.get()


__all__ = ["use_elapsed_time", "format_duration", "ElapsedTimeState"]