"""
Tool pool utilities.

Tool pool management.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class PooledTool:
    """A pooled tool."""
    name: str
    available: bool = True


class ToolPool:
    """Tool pool manager."""

    def __init__(self):
        self._tools: Dict[str, PooledTool] = {}

    def register(self, name: str) -> None:
        """Register a tool."""
        self._tools[name] = PooledTool(name=name)

    def acquire(self, name: str) -> bool:
        """Acquire a tool."""
        if name in self._tools and self._tools[name].available:
            self._tools[name].available = False
            return True
        return False

    def release(self, name: str) -> None:
        """Release a tool."""
        if name in self._tools:
            self._tools[name].available = True


_pool = ToolPool()


def get_tool_pool() -> ToolPool:
    """Get global tool pool."""
    return _pool


__all__ = [
    "PooledTool",
    "ToolPool",
    "get_tool_pool",
]