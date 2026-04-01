"""
Cancel request handler hook.

Python adaptation - handles cancel/escape keybinding.
"""

import time
from typing import Callable, Optional, Any, Dict


# Time window in ms during which a second press kills all background agents
KILL_AGENTS_CONFIRM_WINDOW_MS = 3000


class CancelRequestHandler:
    """Handler for cancel requests."""

    def __init__(self):
        self._last_kill_agents_press = 0.0
        self._abort_signal: Optional[Any] = None
        self._on_cancel: Optional[Callable] = None

    def set_abort_signal(self, abort_signal: Optional[Any]) -> None:
        """Set the abort signal for the current request."""
        self._abort_signal = abort_signal

    def set_on_cancel(self, callback: Callable) -> None:
        """Set the cancel callback."""
        self._on_cancel = callback

    def can_cancel_running_task(self) -> bool:
        """Check if there's a running task that can be cancelled."""
        if self._abort_signal is None:
            return False
        return not getattr(self._abort_signal, "aborted", False)

    def handle_cancel(self) -> None:
        """Handle cancel request."""
        from ..services.analytics import log_event

        log_event("tengu_cancel", {"source": "escape"})

        if self._on_cancel:
            self._on_cancel()

    def handle_interrupt(self) -> None:
        """Handle Ctrl+C interrupt."""
        self.handle_cancel()

    def handle_kill_agents(self, add_notification: Callable, remove_notification: Callable) -> bool:
        """Handle kill agents request.

        Returns True if agents were killed.
        """
        # Check if there are running agents (placeholder - would check actual tasks)
        has_running_agents = False  # Would check store.getState().tasks

        if not has_running_agents:
            add_notification({
                "key": "kill-agents-none",
                "text": "No background agents running",
                "priority": "immediate",
                "timeout_ms": 2000,
            })
            return False

        now = time.time() * 1000  # Convert to milliseconds
        elapsed = now - self._last_kill_agents_press

        if elapsed <= KILL_AGENTS_CONFIRM_WINDOW_MS:
            # Second press within window - kill all agents
            self._last_kill_agents_press = 0
            remove_notification("kill-agents-confirm")
            # Kill all agents (placeholder)
            return True
        else:
            # First press - show confirmation hint
            self._last_kill_agents_press = now
            add_notification({
                "key": "kill-agents-confirm",
                "text": "Press Ctrl+X again to stop background agents",
                "priority": "immediate",
                "timeout_ms": KILL_AGENTS_CONFIRM_WINDOW_MS,
            })
            return False

    def is_escape_active(self, has_queued_commands: bool, is_special_mode: bool = False) -> bool:
        """Check if escape key should be active for cancelling."""
        return (self.can_cancel_running_task() or has_queued_commands) and not is_special_mode

    def is_ctrl_c_active(self, has_queued_commands: bool, is_viewing_teammate: bool = False) -> bool:
        """Check if Ctrl+C should be active."""
        return self.can_cancel_running_task() or has_queued_commands or is_viewing_teammate


# Global instance
_cancel_handler = CancelRequestHandler()


def get_cancel_handler() -> CancelRequestHandler:
    """Get the global cancel handler instance."""
    return _cancel_handler


__all__ = [
    "CancelRequestHandler",
    "get_cancel_handler",
    "KILL_AGENTS_CONFIRM_WINDOW_MS",
]