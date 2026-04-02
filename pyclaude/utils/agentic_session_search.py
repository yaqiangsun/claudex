"""
Agentic session search utilities.

Search for agentic sessions.
"""

from typing import List, Dict, Any, Optional
import os


def search_sessions(
    query: str,
    directory: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search sessions by query.

    Args:
        query: Search query
        directory: Directory to search

    Returns:
        List of matching sessions
    """
    # Placeholder
    return []


def get_session_info(session_id: str) -> Optional[Dict[str, Any]]:
    """Get session information.

    Args:
        session_id: Session ID

    Returns:
        Session info or None
    """
    return None


__all__ = [
    "search_sessions",
    "get_session_info",
]