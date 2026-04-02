"""
Claude.md utilities.

CLAUDE.md file handling.
"""

import os
from typing import Optional, List


def find_claude_md_paths(cwd: str) -> List[str]:
    """Find all CLAUDE.md files in directory tree."""
    paths = []
    for root, dirs, files in os.walk(cwd):
        if "CLAUDE.md" in files:
            paths.append(os.path.join(root, "CLAUDE.md"))
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]
    return paths


def read_claude_md(path: str) -> Optional[str]:
    """Read CLAUDE.md file."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return None


__all__ = [
    "find_claude_md_paths",
    "read_claude_md",
]