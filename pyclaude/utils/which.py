"""
Which utility - find full path to command executable.

Python adaptation using shutil.
"""

import os
import shutil
import sys
import subprocess
from typing import Optional


def which(command: str) -> Optional[str]:
    """Find the full path to a command executable.

    Args:
        command: The command name to look up

    Returns:
        The full path to the command, or None if not found
    """
    # Use shutil.which for cross-platform support
    result = shutil.which(command)
    return result


def which_sync(command: str) -> Optional[str]:
    """Synchronous version of which."""
    return which(command)


async def which_async(command: str) -> Optional[str]:
    """Async version of which."""
    return which(command)


# Windows-specific which using where.exe
def _which_windows(command: str) -> Optional[str]:
    """Windows-specific which using where.exe."""
    try:
        result = subprocess.run(
            f"where.exe {command}",
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not result.stdout:
            return None
        return result.stdout.strip().split("\n")[0]
    except Exception:
        return None


# POSIX-specific which
def _which_posix(command: str) -> Optional[str]:
    """POSIX-specific which using which command."""
    try:
        result = subprocess.run(
            f"which {command}",
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not result.stdout:
            return None
        return result.stdout.strip()
    except Exception:
        return None


# Choose the appropriate implementation based on platform
_which_impl = _which_windows if sys.platform == "win32" else _which_posix


def which_platform(command: str) -> Optional[str]:
    """Platform-specific which implementation."""
    return _which_impl(command)


__all__ = ["which", "which_sync", "which_async", "which_platform"]