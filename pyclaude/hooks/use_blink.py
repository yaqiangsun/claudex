"""
Hook for synchronized blinking animations.

This is a Python adaptation of the React useBlink hook.
Works with textual TUI framework.
"""

import time
from typing import Callable, Optional, Tuple


BLINK_INTERVAL_MS = 600


class BlinkState:
    """Manages blink state for animations."""

    def __init__(self, interval_ms: int = BLINK_INTERVAL_MS):
        self._interval_ms = interval_ms
        self._start_time: Optional[float] = None
        self._enabled = False

    def start(self) -> None:
        """Start the blink animation."""
        self._enabled = True
        self._start_time = time.time()

    def stop(self) -> None:
        """Stop the blink animation."""
        self._enabled = False
        self._start_time = None

    def is_visible(self) -> bool:
        """Check if currently in visible state of blink cycle."""
        if not self._enabled or self._start_time is None:
            return True
        elapsed = (time.time() - self._start_time) * 1000
        return int(elapsed / self._interval_ms) % 2 == 0


# Global blink state instance
_blink_state = BlinkState()


def use_blink(enabled: bool = True, interval_ms: int = BLINK_INTERVAL_MS) -> bool:
    """Use blink hook.

    Returns current visibility state.
    Call start()/stop() on the global instance to control animation.

    Args:
        enabled: Whether blinking is active
        interval_ms: Blink interval in milliseconds

    Returns:
        True when visible in blink cycle
    """
    global _blink_state

    if enabled:
        _blink_state.start()
    else:
        _blink_state.stop()

    return _blink_state.is_visible()


__all__ = ["use_blink", "BlinkState", "BLINK_INTERVAL_MS"]