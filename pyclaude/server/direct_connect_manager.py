"""Direct Connect Manager."""
from typing import Any


class DirectConnectManager:
    """Manages direct connect sessions."""

    def __init__(self):
        self.sessions: dict[str, Any] = {}

    def create_session(self, org_uuid: str, config: dict) -> str:
        """Create a new direct connect session."""
        session_id = config.get('session_id', '')
        self.sessions[session_id] = {
            'session_id': session_id,
            'org_uuid': org_uuid,
            'config': config,
        }
        return session_id

    def get_session(self, session_id: str) -> dict | None:
        """Get a session by ID."""
        return self.sessions.get(session_id)

    def remove_session(self, session_id: str) -> None:
        """Remove a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self) -> list[dict]:
        """List all sessions."""
        return list(self.sessions.values())


__all__ = ['DirectConnectManager']