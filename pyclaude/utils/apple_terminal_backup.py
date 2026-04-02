"""
Apple Terminal backup utilities.

Backup and restore Terminal.app preferences.
"""

import os
import shutil
from typing import Optional


def get_terminal_preferences_path() -> str:
    """Get Terminal.app preferences path."""
    return os.path.expanduser("~/Library/Preferences/com.apple.Terminal.plist")


def backup_terminal_preferences() -> Optional[str]:
    """Backup Terminal preferences."""
    src = get_terminal_preferences_path()
    if not os.path.exists(src):
        return None

    backup = src + ".backup"
    try:
        shutil.copy2(src, backup)
        return backup
    except Exception:
        return None


def restore_terminal_preferences() -> bool:
    """Restore Terminal preferences from backup."""
    src = get_terminal_preferences_path()
    backup = src + ".backup"

    if not os.path.exists(backup):
        return False

    try:
        shutil.copy2(backup, src)
        return True
    except Exception:
        return False


__all__ = [
    "get_terminal_preferences_path",
    "backup_terminal_preferences",
    "restore_terminal_preferences",
]