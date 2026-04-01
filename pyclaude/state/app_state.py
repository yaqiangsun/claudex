"""
App State - Central application state management.

Python adaptation using simple state store pattern.
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(str, Enum):
    """Task status values."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"


@dataclass
class AppState:
    """Main application state."""

    # Messages
    messages: List[Dict[str, Any]] = field(default_factory=list)

    # Tasks
    tasks: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Settings
    settings: Dict[str, Any] = field(default_factory=dict)

    # Model
    main_loop_model: Optional[str] = None

    # Flags
    is_brief_only: bool = False
    is_thinking_enabled: bool = False
    is_loading: bool = False

    # Agent context
    advisor_model: Optional[str] = None

    # Permissions
    tool_permission_context: Dict[str, Any] = field(default_factory=dict)

    # MCP servers
    mcp_servers: Dict[str, Any] = field(default_factory=dict)

    # Plugins
    plugins: List[Dict[str, Any]] = field(default_factory=list)


# Global state
_state: AppState = AppState()
_listeners: List[Callable] = []


def get_default_app_state() -> AppState:
    """Get default application state."""
    return AppState()


def get_state() -> AppState:
    """Get current application state."""
    return _state


def set_state(new_state: AppState) -> None:
    """Set new application state."""
    global _state
    _state = new_state
    _notify_listeners()


def update_state(updater: Callable[[AppState], AppState]) -> None:
    """Update state using a function."""
    global _state
    _state = updater(_state)
    _notify_listeners()


def subscribe(callback: Callable) -> Callable:
    """Subscribe to state changes.

    Returns unsubscribe function.
    """
    _listeners.append(callback)

    def unsubscribe():
        _listeners.remove(callback)

    return unsubscribe


def _notify_listeners() -> None:
    """Notify all listeners of state change."""
    for callback in _listeners:
        callback(_state)


# Re-export for compatibility
__all__ = [
    "AppState",
    "TaskStatus",
    "get_state",
    "set_state",
    "update_state",
    "subscribe",
    "get_default_app_state",
]