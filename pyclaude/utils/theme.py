"""
Theme utilities.

Theme handling.
"""

from typing import Dict, Any


def get_theme() -> str:
    """Get current theme."""
    import os
    return os.environ.get("CLAUDE_CODE_THEME", "dark")


def get_theme_colors(theme: str) -> Dict[str, str]:
    """Get theme colors."""
    themes = {
        "dark": {
            "background": "#1e1e1e",
            "foreground": "#d4d4d4",
        },
        "light": {
            "background": "#ffffff",
            "foreground": "#1e1e1e",
        },
    }
    return themes.get(theme, themes["dark"])


__all__ = [
    "get_theme",
    "get_theme_colors",
]