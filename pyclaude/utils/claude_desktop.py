"""
Claude Desktop utilities.

Claude Desktop integration.
"""

import os
import subprocess
from typing import Optional


def get_claude_desktop_path() -> str:
    """Get Claude Desktop app path."""
    if os.path.exists("/Applications/Claude.app"):
        return "/Applications/Claude.app"
    return ""


def is_claude_desktop_running() -> bool:
    """Check if Claude Desktop is running."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "Claude"],
            capture_output=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def open_in_desktop(path: str) -> bool:
    """Open path in Claude Desktop."""
    if os.path.exists("/Applications/Claude.app"):
        subprocess.run(["open", "-a", "Claude", path])
        return True
    return False


__all__ = [
    "get_claude_desktop_path",
    "is_claude_desktop_running",
    "open_in_desktop",
]