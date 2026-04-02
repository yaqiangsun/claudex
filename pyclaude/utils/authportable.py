"""
Auth portable utility.

Portable authentication utilities.
"""

import os
from typing import Optional


def get_portable_auth_path() -> Optional[str]:
    """Get portable auth path."""
    return os.environ.get('CLAUDE_CODE_PORTABLE_AUTH_PATH')


def is_portable_mode() -> bool:
    """Check if running in portable mode."""
    return get_portable_auth_path() is not None


def load_portable_auth() -> Optional[dict]:
    """Load portable authentication data."""
    auth_path = get_portable_auth_path()
    if not auth_path:
        return None
    import json
    try:
        with open(auth_path) as f:
            return json.load(f)
    except Exception:
        return None


__all__ = ['get_portable_auth_path', 'is_portable_mode', 'load_portable_auth']