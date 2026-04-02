"""
Agentic session search utility.

Search for agentic sessions.
"""

from typing import Optional, List, Dict, Any


class AgenticSessionSearch:
    """Search for agentic sessions."""

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def add_session(self, session_id: str, data: Dict[str, Any]) -> None:
        """Add a session."""
        self._sessions[session_id] = data

    def find_session(self, query: str) -> Optional[str]:
        """Find a session by query."""
        for session_id, data in self._sessions.items():
            if query.lower() in str(data).lower():
                return session_id
        return None

    def list_sessions(self) -> List[str]:
        """List all session IDs."""
        return list(self._sessions.keys())


# Global instance
_session_search = AgenticSessionSearch()


def get_agentic_session_search() -> AgenticSessionSearch:
    """Get global session search."""
    return _session_search


__all__ = ['AgenticSessionSearch', 'get_agentic_session_search']