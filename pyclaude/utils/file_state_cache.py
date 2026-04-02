"""
File state cache utilities.

Cache file state.
"""

import os
import time
from typing import Dict, Any, Optional


_file_cache: Dict[str, tuple] = {}


def cache_file_state(path: str, state: Dict[str, Any]) -> None:
    """Cache file state."""
    _file_cache[path] = (state, time.time())


def get_file_state(path: str, ttl: int = 60) -> Optional[Dict[str, Any]]:
    """Get cached file state."""
    if path in _file_cache:
        state, timestamp = _file_cache[path]
        if time.time() - timestamp < ttl:
            return state
    return None


__all__ = [
    "cache_file_state",
    "get_file_state",
]