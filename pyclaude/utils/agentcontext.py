"""
Agent context utility.

Agent context management.
"""

from contextvars import ContextVar
from typing import Optional, Dict, Any


# Context variable for agent ID
_current_agent_id: ContextVar[Optional[str]] = ContextVar('agent_id', default=None)
_current_agent_data: ContextVar[Optional[Dict[str, Any]]] = ContextVar('agent_data', default=None)


def set_agent_context(agent_id: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Set the current agent context."""
    _current_agent_id.set(agent_id)
    _current_agent_data.set(data or {})


def get_agent_id() -> Optional[str]:
    """Get current agent ID."""
    return _current_agent_id.get()


def get_agent_data() -> Optional[Dict[str, Any]]:
    """Get current agent data."""
    return _current_agent_data.get()


def clear_agent_context() -> None:
    """Clear the current agent context."""
    _current_agent_id.set(None)
    _current_agent_data.set(None)


class AgentContext:
    """Agent context manager."""

    def __init__(self, agent_id: str, data: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.data = data or {}
        self._prev_id = None
        self._prev_data = None

    def __enter__(self):
        self._prev_id = get_agent_id()
        self._prev_data = get_agent_data()
        set_agent_context(self.agent_id, self.data)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _current_agent_id.set(self._prev_id)
        _current_agent_data.set(self._prev_data)


__all__ = ['set_agent_context', 'get_agent_id', 'get_agent_data', 'clear_agent_context', 'AgentContext']