"""
Tool result storage utilities.

Store tool results.
"""

import json
import os
from typing import Optional, Any


def store_tool_result(tool_name: str, result: Any) -> str:
    """Store tool result."""
    cache_dir = os.environ.get("CLAUDE_CODE_CACHE_DIR", "/tmp/claude-cache")
    path = os.path.join(cache_dir, "results", f"{tool_name}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(result, f)
    return path


def load_tool_result(tool_name: str) -> Optional[Any]:
    """Load tool result."""
    cache_dir = os.environ.get("CLAUDE_CODE_CACHE_DIR", "/tmp/claude-cache")
    path = os.path.join(cache_dir, "results", f"{tool_name}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


__all__ = [
    "store_tool_result",
    "load_tool_result",
]