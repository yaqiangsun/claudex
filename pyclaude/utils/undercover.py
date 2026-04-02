"""
Undercover utilities.

Undercover mode handling.
"""

import os


def is_undercover_enabled() -> bool:
    """Check if undercover mode is enabled."""
    return os.environ.get("CLAUDE_CODE_UNDERCOVER", "").lower() == "true"


def get_undercover_config() -> dict:
    """Get undercover configuration."""
    return {
        "enabled": is_undercover_enabled(),
    }


__all__ = [
    "is_undercover_enabled",
    "get_undercover_config",
]