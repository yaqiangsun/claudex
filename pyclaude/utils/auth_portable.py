"""
Portable auth utilities for different platforms.
"""

import os
import subprocess


def maybe_remove_api_key_from_mac_os_keychain_throws() -> None:
    """Remove API key from macOS keychain."""
    if os.name == 'posix' and os.uname().sysname == 'Darwin':
        # Would use keychain API
        pass


def normalize_api_key_for_config(api_key: str) -> str:
    """Normalize API key for config display (show last 20 chars)."""
    return api_key[-20:] if len(api_key) > 20 else api_key


__all__ = [
    "maybe_remove_api_key_from_mac_os_keychain_throws",
    "normalize_api_key_for_config",
]