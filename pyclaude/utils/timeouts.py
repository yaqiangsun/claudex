"""
Timeouts utilities.

Timeout configuration.
"""

from typing import Dict


DEFAULT_TIMEOUTS: Dict[str, int] = {
    "default": 30000,
    "tool": 60000,
    "api": 30000,
}


def get_timeout(key: str = "default") -> int:
    """Get timeout value."""
    import os
    env_timeout = os.environ.get(f"CLAUDE_CODE_TIMEOUT_{key.upper()}")
    if env_timeout:
        try:
            return int(env_timeout)
        except ValueError:
            pass
    return DEFAULT_TIMEOUTS.get(key, 30000)


__all__ = [
    "DEFAULT_TIMEOUTS",
    "get_timeout",
]