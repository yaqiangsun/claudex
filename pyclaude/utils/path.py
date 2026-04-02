"""
Path utilities.

Python adaptation.
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_platform() -> str:
    """Get the current platform."""
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "darwin"
    return "linux"


def expand_path(path: str, base_dir: Optional[str] = None) -> str:
    """Expand a path that may contain tilde notation (~) to an absolute path.

    Args:
        path: The path to expand
        base_dir: Base directory for resolving relative paths

    Returns:
        Expanded absolute path
    """
    actual_base_dir = base_dir or os.getcwd()

    # Input validation
    if not isinstance(path, str):
        raise TypeError(f"Path must be a string, received {type(path)}")

    if not isinstance(actual_base_dir, str):
        raise TypeError(f"Base directory must be a string, received {type(actual_base_dir)}")

    # Security: Check for null bytes
    if "\0" in path or "\0" in actual_base_dir:
        raise ValueError("Path contains null bytes")

    # Handle empty or whitespace-only paths
    trimmed_path = path.strip()
    if not trimmed_path:
        return os.path.normpath(actual_base_dir)

    # Handle home directory notation
    home = str(Path.home())
    if trimmed_path == "~":
        return os.path.normpath(home)

    if trimmed_path.startswith("~/"):
        full_path = os.path.join(home, trimmed_path[2:])
        return os.path.normpath(full_path)

    # Handle absolute paths
    if os.path.isabs(trimmed_path):
        return os.path.normpath(trimmed_path)

    # Handle relative paths
    full_path = os.path.join(actual_base_dir, trimmed_path)
    return os.path.normpath(full_path)


def to_relative_path(absolute_path: str) -> str:
    """Convert absolute path to relative path from current directory."""
    try:
        return os.path.relpath(absolute_path)
    except ValueError:
        return absolute_path


def get_directory_for_path(path: str) -> str:
    """Get the directory containing a path."""
    return os.path.dirname(os.path.abspath(path))


def contains_path_traversal(path: str) -> bool:
    """Check if path contains path traversal sequences."""
    # Normalize and check
    normalized = os.path.normpath(path)
    # Check for .. that would traverse up
    parts = normalized.split(os.sep)
    return ".." in parts


def normalize_path_for_config_key(path: str) -> str:
    """Normalize path for use as a config key."""
    # Replace problematic characters
    return path.replace("/", "_").replace("\\", "_").replace(":", "_")


__all__ = [
    "get_platform",
    "expand_path",
    "to_relative_path",
    "get_directory_for_path",
    "contains_path_traversal",
    "normalize_path_for_config_key",
]