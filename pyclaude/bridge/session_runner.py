"""Session runner - manages session execution in bridge mode."""

import asyncio
from typing import Any, Callable, Optional, Dict
from dataclasses import dataclass
from enum import Enum

from .types import SessionInfo, BridgeState


class SessionState(str, Enum):
    """Session state."""
    PENDING = 'pending'
    RUNNING = 'running'
    PAUSED = 'paused'
    COMPLETED = 'completed'
    FAILED = 'failed'


@dataclass
class SessionConfig:
    """Configuration for a session."""
    session_id: str
    cwd: str
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    tools: list = None
    timeout: Optional[int] = None


class SessionRunner:
    """Manages session execution."""

    def __init__(self):
        self._sessions: Dict[str, SessionInfo] = {}
        self._running: Dict[str, asyncio.Task] = {}
        self._state_callbacks: Dict[str, Callable] = {}

    async def create_session(self, config: SessionConfig) -> SessionInfo:
        """Create a new session."""
        import time
        import uuid

        session = SessionInfo(
            id=config.session_id or str(uuid.uuid4()),
            created_at=int(time.time() * 1000),
            last_active=int(time.time() * 1000),
            status='pending',
        )

        self._sessions[session.id] = session
        return session

    async def start_session(self, session_id: str) -> bool:
        """Start a session."""
        session = self._sessions.get(session_id)
        if not session:
            return False

        session.status = 'active'
        session.last_active = int(asyncio.get_event_loop().time() * 1000)

        # In a real implementation, this would start the actual session
        # For now, just mark it as running
        return True

    async def pause_session(self, session_id: str) -> bool:
        """Pause a session."""
        session = self._sessions.get(session_id)
        if not session:
            return False

        session.status = 'paused'
        return True

    async def resume_session(self, session_id: str) -> bool:
        """Resume a paused session."""
        session = self._sessions.get(session_id)
        if not session or session.status != 'paused':
            return False

        session.status = 'active'
        session.last_active = int(asyncio.get_event_loop().time() * 1000)
        return True

    async def stop_session(self, session_id: str) -> bool:
        """Stop a session."""
        session = self._sessions.get(session_id)
        if not session:
            return False

        session.status = 'completed'

        # Cancel running task if any
        if session_id in self._running:
            task = self._running.pop(session_id)
            task.cancel()

        return True

    def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """Get a session by ID."""
        return self._sessions.get(session_id)

    def list_sessions(self) -> list[SessionInfo]:
        """List all sessions."""
        return list(self._sessions.values())


# Global session runner
_runner = SessionRunner()


def get_session_runner() -> SessionRunner:
    """Get the global session runner."""
    return _runner


__all__ = [
    'SessionRunner',
    'SessionConfig',
    'SessionState',
    'get_session_runner',
]