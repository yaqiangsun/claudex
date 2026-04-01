"""
Session-scoped environment variables set via /env.

Applied only to spawned child processes (via bash provider env overrides),
not to the REPL process itself.
"""

from typing import Dict, ReadOnly


# Session-scoped environment variables
_session_env_vars: Dict[str, str] = {}


def get_session_env_vars() -> Dict[str, str]:
    """Get all session environment variables."""
    return _session_env_vars.copy()


def set_session_env_var(name: str, value: str) -> None:
    """Set a session environment variable."""
    _session_env_vars[name] = value


def delete_session_env_var(name: str) -> None:
    """Delete a session environment variable."""
    _session_env_vars.pop(name, None)


def clear_session_env_vars() -> None:
    """Clear all session environment variables."""
    _session_env_vars.clear()


__all__ = [
    "get_session_env_vars",
    "set_session_env_var",
    "delete_session_env_var",
    "clear_session_env_vars",
]