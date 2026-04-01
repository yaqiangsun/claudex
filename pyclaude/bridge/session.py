"""
Session management for bridge.
"""

import asyncio
import secrets
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Optional, Union
from datetime import datetime


@dataclass
class Session:
    """Represents a bridge session."""
    id: str
    name: Optional[str] = None
    created_at: int = 0
    last_active: int = 0
    status: str = 'active'
    metadata: dict = field(default_factory=dict)
    client_info: Optional[dict] = None

    def __post_init__(self):
        if self.created_at == 0:
            import time
            self.created_at = int(time.time() * 1000)
        if self.last_active == 0:
            self.last_active = self.created_at

    def update_activity(self) -> None:
        """Update last active timestamp."""
        import time
        self.last_active = int(time.time() * 1000)

    def is_active(self) -> bool:
        """Check if session is active."""
        return self.status == 'active'

    def end(self) -> None:
        """End the session."""
        self.status = 'ended'


class SessionManager:
    """Manages bridge sessions."""

    def __init__(self):
        self._sessions: dict[str, Session] = {}
        self._lock = asyncio.Lock()

    async def create_session(
        self,
        name: Optional[str] = None,
        client_info: Optional[dict] = None,
    ) -> Session:
        """Create a new session."""
        async with self._lock:
            session_id = self._generate_session_id()
            session = Session(
                id=session_id,
                name=name,
                client_info=client_info,
            )
            self._sessions[session_id] = session
            return session

    async def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        async with self._lock:
            return self._sessions.get(session_id)

    async def list_sessions(self) -> list[Session]:
        """List all active sessions."""
        async with self._lock:
            return [
                s for s in self._sessions.values()
                if s.status == 'active'
            ]

    async def end_session(self, session_id: str) -> bool:
        """End a session."""
        async with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session.end()
                return True
            return False

    async def cleanup_inactive(self, timeout_ms: int = 300000) -> int:
        """Clean up inactive sessions."""
        import time
        current_time = int(time.time() * 1000)
        cleaned = 0

        async with self._lock:
            to_remove = []
            for session in self._sessions.values():
                if session.status == 'active':
                    if current_time - session.last_active > timeout_ms:
                        session.end()
                        to_remove.append(session.id)
                        cleaned += 1

            for session_id in to_remove:
                del self._sessions[session_id]

        return cleaned

    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return secrets.token_hex(16)


# Session message handler
class SessionRunner:
    """Runs sessions for bridge."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the session runner."""
        self._running = True
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        """Stop the session runner."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run(self) -> None:
        """Main runner loop."""
        while self._running:
            # Cleanup inactive sessions every 60 seconds
            await asyncio.sleep(60)
            await self.session_manager.cleanup_inactive()


__all__ = ['Session', 'SessionManager', 'SessionRunner']