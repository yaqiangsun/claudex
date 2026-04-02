"""
Query helpers utilities.

Query helper functions.
"""

from typing import Any, Optional, Dict


def normalize_query(query: str) -> str:
    """Normalize query text."""
    return query.strip()


def extract_query_intent(query: str) -> str:
    """Extract query intent."""
    query_lower = query.lower()
    if "write" in query_lower or "create" in query_lower:
        return "create"
    if "edit" in query_lower or "modify" in query_lower:
        return "edit"
    if "read" in query_lower or "show" in query_lower:
        return "read"
    return "general"


__all__ = [
    "normalize_query",
    "extract_query_intent",
]