"""Remote service - handles remote sessions."""

import asyncio
import uuid
from typing import Any, Callable, Optional, Dict
from dataclasses import dataclass, field
from enum import Enum


class RemoteSessionState(str, Enum):
    """Remote session states."""
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
    ERROR = 'error'


@dataclass
class RemoteSession:
    """A remote session."""
    id: str
    state: RemoteSessionState = RemoteSessionState.DISCONNECTED
    host: str = ''
    port: int = 0
    created_at: float = field(default_factory=lambda: asyncio.get_event_loop().time())


class RemoteService:
    """Service for managing remote sessions."""

    def __init__(self):
        self._sessions: Dict[str, RemoteSession] = {}
        self._connection_callbacks: Dict[str, Callable] = {}

    async def connect(self, host: str, port: int = 3100) -> RemoteSession:
        """Connect to a remote session."""
        session_id = str(uuid.uuid4())

        session = RemoteSession(
            id=session_id,
            state=RemoteSessionState.CONNECTING,
            host=host,
            port=port,
        )

        self._sessions[session_id] = session

        # Simulate connection
        await asyncio.sleep(0.1)
        session.state = RemoteSessionState.CONNECTED

        return session

    async def disconnect(self, session_id: str) -> bool:
        """Disconnect from a remote session."""
        session = self._sessions.get(session_id)
        if not session:
            return False

        session.state = RemoteSessionState.DISCONNECTED
        return True

    def get_session(self, session_id: str) -> Optional[RemoteSession]:
        """Get a session by ID."""
        return self._sessions.get(session_id)

    def list_sessions(self) -> list[RemoteSession]:
        """List all remote sessions."""
        return [
            s for s in self._sessions.values()
            if s.state == RemoteSessionState.CONNECTED
        ]


# Global service instance
_remote_service = RemoteService()


def get_remote_service() -> RemoteService:
    """Get the global remote service."""
    return _remote_service


__all__ = ['RemoteService', 'RemoteSession', 'RemoteSessionState', 'get_remote_service']