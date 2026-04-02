"""
Memory file detection utilities.

Detect memory files.
"""

import os
from typing import List


def detect_memory_files(directory: str) -> List[str]:
    """Detect memory files in directory."""
    memory_files = []
    for filename in ["CLAUDE.md", "CLAUDE.local.md", "CLAUDE.md.bak"]:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            memory_files.append(path)
    return memory_files


__all__ = ["detect_memory_files"]