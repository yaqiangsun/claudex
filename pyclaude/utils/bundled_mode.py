"""
Detects if the current runtime is Bun.

Note: This is for Bun runtime - Python equivalent would be checking for
PyInstaller or similar bundling.
"""

import sys


def is_running_with_bun() -> bool:
    """Check if running with Bun runtime."""
    # Python equivalent - check if running as bundled executable
    return getattr(sys, 'frozen', False)


def is_in_bundled_mode() -> bool:
    """Check if running as a bundled executable."""
    return getattr(sys, 'frozen', False)


__all__ = ["is_running_with_bun", "is_in_bundled_mode"]