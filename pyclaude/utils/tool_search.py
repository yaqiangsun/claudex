"""
Tool search utilities.

Search for tools.
"""

from typing import List, Dict, Any


def search_tools(query: str, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Search tools by query."""
    query_lower = query.lower()
    return [
        t for t in tools
        if query_lower in t.get("name", "").lower()
        or query_lower in t.get("description", "").lower()
    ]


__all__ = ["search_tools"]