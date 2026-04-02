"""
File utilities.

File operations.
"""

import os
from typing import Optional


def file_exists(path: str) -> bool:
    """Check if file exists."""
    return os.path.exists(path)


def read_file(path: str) -> Optional[str]:
    """Read file content."""
    try:
        with open(path) as f:
            return f.read()
    except Exception:
        return None


__all__ = [
    "file_exists",
    "read_file",
]