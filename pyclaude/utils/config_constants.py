"""
Configuration constants.

These constants are in a separate file to avoid circular dependency issues.
Do NOT add imports to this file - it must remain dependency-free.
"""

from typing import Tuple

NOTIFICATION_CHANNELS: Tuple[str, ...] = (
    'auto',
    'iterm2',
    'iterm2_with_bell',
    'terminal_bell',
    'kitty',
    'ghostty',
    'notifications_disabled',
)

# Valid editor modes (excludes deprecated 'emacs' which is auto-migrated to 'normal')
EDITOR_MODES: Tuple[str, ...] = ('normal', 'vim')

# Valid teammate modes for spawning
# 'tmux' = traditional tmux-based teammates
# 'in-process' = in-process teammates running in same process
# 'auto' = automatically choose based on context (default)
TEAMMATE_MODES: Tuple[str, ...] = ('auto', 'tmux', 'in-process')


__all__ = [
    "NOTIFICATION_CHANNELS",
    "EDITOR_MODES",
    "TEAMMATE_MODES",
]