"""
Session ingress auth utilities.

Session ingress authentication.
"""

from typing import Optional


def validate_ingress_token(token: str) -> bool:
    """Validate ingress token."""
    # Placeholder
    return len(token) > 0


def get_ingress_token() -> Optional[str]:
    """Get ingress token from environment."""
    import os
    return os.environ.get("CLAUDE_CODE_INGRESS_TOKEN")


__all__ = [
    "validate_ingress_token",
    "get_ingress_token",
]