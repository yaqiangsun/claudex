"""
Idle timeout utilities.

Handle idle timeout.
"""

import time
from typing import Optional, Callable


class IdleTimeout:
    """Track idle time."""

    def __init__(self, timeout_seconds: int = 300):
        self.timeout = timeout_seconds
        self.last_activity = time.time()

    def reset(self) -> None:
        """Reset idle timer."""
        self.last_activity = time.time()

    def get_idle_time(self) -> float:
        """Get idle time in seconds."""
        return time.time() - self.last_activity

    def is_timed_out(self) -> bool:
        """Check if timed out."""
        return self.get_idle_time() > self.timeout


_timeout = IdleTimeout()


def get_idle_timeout() -> IdleTimeout:
    """Get global idle timeout."""
    return _timeout


__all__ = [
    "IdleTimeout",
    "get_idle_timeout",
]