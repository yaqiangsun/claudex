"""
System theme utilities.

System theme detection.
"""

import os


def get_system_theme() -> str:
    """Get system theme (dark/light)."""
    # Placeholder - would detect from terminal
    return os.environ.get("CLAUDE_CODE_THEME", "dark")


__all__ = ["get_system_theme"]