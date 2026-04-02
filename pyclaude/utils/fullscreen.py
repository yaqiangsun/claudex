"""
Fullscreen utilities.

Terminal fullscreen handling.
"""

import os


def is_fullscreen() -> bool:
    """Check if terminal is fullscreen."""
    return os.environ.get("TERM_FULLSCREEN", "").lower() == "true"


def enable_fullscreen() -> None:
    """Enable fullscreen mode."""
    os.environ["TERM_FULLSCREEN"] = "true"


def disable_fullscreen() -> None:
    """Disable fullscreen mode."""
    os.environ.pop("TERM_FULLSCREEN", None)


__all__ = [
    "is_fullscreen",
    "enable_fullscreen",
    "disable_fullscreen",
]