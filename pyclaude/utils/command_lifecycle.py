"""
Command lifecycle tracking.
"""

from typing import Callable, Optional, Dict

CommandLifecycleState = str  # 'started' | 'completed'
CommandLifecycleListener = Callable[[str, CommandLifecycleState], None]

_listener: Optional[CommandLifecycleListener] = None


def set_command_lifecycle_listener(cb: Optional[CommandLifecycleListener]) -> None:
    """Set the command lifecycle listener."""
    global _listener
    _listener = cb


def notify_command_lifecycle(uuid: str, state: CommandLifecycleState) -> None:
    """Notify command lifecycle state change."""
    if _listener:
        _listener(uuid, state)


__all__ = [
    "CommandLifecycleState",
    "CommandLifecycleListener",
    "set_command_lifecycle_listener",
    "notify_command_lifecycle",
]