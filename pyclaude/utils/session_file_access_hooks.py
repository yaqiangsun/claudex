"""
Session file access hooks utilities.

File access hooks for sessions.
"""

from typing import Callable, List


_hooks: List[Callable] = []


def register_file_access_hook(hook: Callable) -> None:
    """Register file access hook."""
    _hooks.append(hook)


def trigger_file_access_hook(path: str) -> None:
    """Trigger file access hooks."""
    for hook in _hooks:
        try:
            hook(path)
        except Exception:
            pass


__all__ = [
    "register_file_access_hook",
    "trigger_file_access_hook",
]