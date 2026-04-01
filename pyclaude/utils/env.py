"""Environment utilities."""

import os
import platform
from typing import Optional

Platform = str  # 'win32' | 'darwin' | 'linux'


def get_platform() -> Platform:
    """Get the current platform."""
    return platform.system().lower()


def is_darwin() -> bool:
    """Check if running on macOS."""
    return platform.system() == 'Darwin'


def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == 'Linux'


def is_win32() -> bool:
    """Check if running on Windows."""
    return platform.system() == 'Windows'


def get_home_dir() -> str:
    """Get the user's home directory."""
    return os.path.expanduser('~')


def is_env_truthy(value: Optional[str]) -> bool:
    """Check if env value is truthy."""
    return value is not None and value.lower() in ('1', 'true', 'yes')