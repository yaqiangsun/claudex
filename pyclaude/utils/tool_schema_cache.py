"""
Tool schema cache utilities.

Cache tool schemas.
"""

from typing import Optional, Dict, Any


_schema_cache: Dict[str, Any] = {}


def get_tool_schema_cache() -> Dict[str, Any]:
    """Get tool schema cache."""
    return _schema_cache


def cache_tool_schema(name: str, schema: Any) -> None:
    """Cache tool schema."""
    _schema_cache[name] = schema


__all__ = [
    "get_tool_schema_cache",
    "cache_tool_schema",
]