"""
Team memory operations utilities.

Team memory operations.
"""

from typing import Optional, Dict, Any


def read_team_memory(path: str) -> Optional[str]:
    """Read team memory."""
    try:
        with open(path) as f:
            return f.read()
    except Exception:
        return None


def write_team_memory(path: str, content: str) -> bool:
    """Write team memory."""
    try:
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return True
    except Exception:
        return False


__all__ = [
    "read_team_memory",
    "write_team_memory",
]