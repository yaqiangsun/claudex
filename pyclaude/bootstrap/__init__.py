"""Bootstrap module - initialization and state."""

import os
from typing import Any

# Global state
_initialized = False
_cwd: str = ''


def initialize_state(cwd: str) -> None:
    """Initialize the application state."""
    global _initialized, _cwd
    _cwd = cwd
    _initialized = True


def is_initialized() -> bool:
    """Check if state is initialized."""
    return _initialized


def get_cwd() -> str:
    """Get current working directory."""
    return _cwd or os.getcwd()


def is_session_persistence_disabled() -> bool:
    """Check if session persistence is disabled."""
    return os.environ.get('CLAUDE_DISABLE_PERSISTENCE') == 'true'


__all__ = [
    'initialize_state',
    'is_initialized',
    'get_cwd',
    'is_session_persistence_disabled',
]