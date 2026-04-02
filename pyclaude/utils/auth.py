"""
Authentication utilities.
"""

import os
from typing import Optional, Tuple


def get_anthropic_api_key() -> Optional[str]:
    """Get the Anthropic API key."""
    key, _ = get_anthropic_api_key_with_source()
    return key


def is_anthropic_auth_enabled() -> bool:
    """Check if Anthropic authentication is enabled."""
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY"))


def is_claude_ai_subscriber() -> bool:
    """Check if user is a Claude AI subscriber."""
    return os.environ.get("CLAUDE_AI_SUBSCRIBER", "").lower() == "true"


def get_anthropic_api_key_with_source(
    skip_retrieving_key_from_api_key_helper: bool = False,
) -> Tuple[Optional[str], str]:
    """Get Anthropic API key and its source.

    Returns:
        Tuple of (api_key, source)
    """
    # Check environment variables first
    key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY")
    if key:
        return key, "env"

    # Check config file
    config_key = os.environ.get("CLAUDE_API_KEY_FROM_CONFIG")
    if config_key:
        return config_key, "config"

    # Check apiKeyHelper (skipped by default for security)
    if not skip_retrieving_key_from_api_key_helper:
        helper_key = os.environ.get("CLAUDE_CODE_API_KEY_HELPER")
        if helper_key:
            return helper_key, "apiKeyHelper"

    return None, "none"


async def get_api_key_from_api_key_helper(is_non_interactive: bool) -> Optional[str]:
    """Get API key from the configured helper."""
    helper = os.environ.get("CLAUDE_CODE_API_KEY_HELPER")
    if not helper:
        return None

    # Execute the helper (placeholder - would run shell command)
    return None


__all__ = [
    "get_anthropic_api_key",
    "is_anthropic_auth_enabled",
    "is_claude_ai_subscriber",
    "get_anthropic_api_key_with_source",
    "get_api_key_from_api_key_helper",
]