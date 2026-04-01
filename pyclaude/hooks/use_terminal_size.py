"""
Terminal size hook - get terminal dimensions.

Python adaptation for textual TUI.
"""

import os
from typing import Tuple, Optional


def get_terminal_size() -> Tuple[int, int]:
    """Get terminal size as (rows, columns)."""
    try:
        import shutil
        size = shutil.get_terminal_size(fallback=(80, 24))
        return (size.lines, size.columns)
    except Exception:
        return (24, 80)


def use_terminal_size() -> Tuple[int, int]:
    """Hook to get terminal size."""
    return get_terminal_size()


__all__ = ["use_terminal_size", "get_terminal_size"]