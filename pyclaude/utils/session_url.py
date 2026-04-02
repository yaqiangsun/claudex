"""
Session URL utilities.

Session URL handling.
"""

from typing import Optional


def get_session_url(session_id: str) -> str:
    """Get session URL."""
    return f"claude://session/{session_id}"


def parse_session_url(url: str) -> Optional[str]:
    """Parse session ID from URL."""
    if url.startswith("claude://session/"):
        return url.split("/")[-1]
    return None


__all__ = [
    "get_session_url",
    "parse_session_url",
]