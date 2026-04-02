"""
List sessions implementation utilities.

List sessions implementation.
"""

import os
from typing import List, Dict, Any, Optional


def list_sessions_impl(directory: Optional[str] = None) -> List[Dict[str, Any]]:
    """List sessions from directory."""
    if directory is None:
        directory = os.path.expanduser("~/.config/claude/projects")

    sessions = []
    if os.path.exists(directory):
        for entry in os.listdir(directory):
            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                sessions.append({
                    "id": entry,
                    "path": path,
                })
    return sessions


__all__ = ["list_sessions_impl"]