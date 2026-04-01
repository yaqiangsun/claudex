"""
Command queue hook - subscribe to the unified command queue.

Python adaptation - manages queued commands.
"""

from typing import List, Dict, Any, Callable, Set
from dataclasses import dataclass


@dataclass
class QueuedCommand:
    """A queued command."""
    id: str
    command: str
    args: str


# Command queue storage
_command_queue: List[QueuedCommand] = []
_subscribers: Set[Callable] = set()


def get_command_queue_snapshot() -> List[QueuedCommand]:
    """Get a copy of the current command queue."""
    return _command_queue.copy()


def subscribe_to_command_queue(callback: Callable) -> Callable:
    """Subscribe to command queue changes.

    Returns unsubscribe function.
    """
    _subscribers.add(callback)

    def unsubscribe():
        _subscribers.discard(callback)

    return unsubscribe


def enqueue_command(command: QueuedCommand) -> None:
    """Add a command to the queue."""
    _command_queue.append(command)
    _notify_subscribers()


def dequeue_command() -> QueuedCommand:
    """Remove and return the first command."""
    if _command_queue:
        cmd = _command_queue.pop(0)
        _notify_subscribers()
        return cmd
    raise IndexError("Command queue is empty")


def _notify_subscribers() -> None:
    """Notify all subscribers of queue change."""
    for callback in _subscribers:
        callback()


def use_command_queue() -> List[QueuedCommand]:
    """Hook to get the current command queue."""
    return get_command_queue_snapshot()


__all__ = [
    "QueuedCommand",
    "use_command_queue",
    "get_command_queue_snapshot",
    "subscribe_to_command_queue",
    "enqueue_command",
    "dequeue_command",
]