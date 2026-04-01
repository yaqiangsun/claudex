"""
Timeout hook - simple timer that tracks if delay has elapsed.
"""

import time
from typing import Optional


class TimeoutState:
    """Manages timeout state."""

    def __init__(self):
        self._start_time: Optional[float] = None
        self._delay: float = 0
        self._reset_trigger: Optional[int] = None
        self._elapsed = False

    def check(self, delay: float, reset_trigger: Optional[int] = None) -> bool:
        """Check if timeout has elapsed."""
        if reset_trigger != self._reset_trigger:
            # Reset triggered - start new timer
            self._start_time = time.time()
            self._delay = delay
            self._reset_trigger = reset_trigger
            self._elapsed = False

        if self._start_time is None:
            self._start_time = time.time()
            return False

        elapsed = (time.time() - self._start_time) * 1000  # ms
        self._elapsed = elapsed >= self._delay
        return self._elapsed


# Global state
_timeout_state = TimeoutState()


def use_timeout(delay: float, reset_trigger: Optional[int] = None) -> bool:
    """Hook that returns True after delay milliseconds have passed."""
    return _timeout_state.check(delay, reset_trigger)


__all__ = ["use_timeout", "TimeoutState"]