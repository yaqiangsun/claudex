"""
Auto updater utility.

Automatic update utilities.
"""

import os
from typing import Optional


def is_auto_update_enabled() -> bool:
    """Check if auto update is enabled."""
    env = os.environ.get('CLAUDE_CODE_AUTO_UPDATE', 'true').lower()
    return env in ('true', '1', 'yes')


def get_auto_update_channel() -> str:
    """Get auto update channel."""
    return os.environ.get('CLAUDE_CODE_UPDATE_CHANNEL', 'stable')


async def check_for_updates() -> Optional[dict]:
    """Check for updates."""
    # Placeholder
    return None


async def apply_update(version: str) -> bool:
    """Apply an update."""
    # Placeholder
    return False


__all__ = ['is_auto_update_enabled', 'get_auto_update_channel', 'check_for_updates', 'apply_update']