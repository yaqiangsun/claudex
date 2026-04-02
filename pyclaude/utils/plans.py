"""
Plans utilities.

Plan file handling.
"""

import os
from typing import Optional, Dict, Any


def get_plan_file_path(agent_id: Optional[str] = None) -> str:
    """Get plan file path."""
    config_dir = os.environ.get("CLAUDE_CONFIG_HOME", os.path.expanduser("~/.config/claude"))
    if agent_id:
        return os.path.join(config_dir, "plans", f"{agent_id}.md")
    return os.path.join(config_dir, "plans", "current.md")


def get_plan(agent_id: Optional[str] = None) -> Optional[str]:
    """Get plan content."""
    path = get_plan_file_path(agent_id)
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return None


__all__ = [
    "get_plan_file_path",
    "get_plan",
]