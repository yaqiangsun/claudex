"""
Stats cache utilities.

Stats caching.
"""

from typing import Optional, Dict, Any
import time


_cache: Dict[str, Any] = {}
_cache_time: Dict[str, float] = {}


def cache_stats(key: str, value: Any, ttl_seconds: int = 60) -> None:
    """Cache stats."""
    _cache[key] = value
    _cache_time[key] = time.time() + ttl_seconds


def get_cached_stats(key: str) -> Optional[Any]:
    """Get cached stats."""
    if key in _cache and key in _cache_time:
        if time.time() < _cache_time[key]:
            return _cache[key]
    return None


__all__ = [
    "cache_stats",
    "get_cached_stats",
]