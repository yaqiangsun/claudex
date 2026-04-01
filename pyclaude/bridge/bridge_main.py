"""
Bridge Main - Main bridge implementation.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Union

from .types import (
    BridgeConfig,
    BridgeState,
    BridgeMessage,
    BridgeEvent,
    BridgeEventType,
    SessionInfo,
)
from .repl_bridge import REPLBridge, REPLBridgeConfig


@dataclass
class BridgeMain:
    """
    Main bridge controller.
    Manages the always-on bridge for remote control.
    """

    config: BridgeConfig = field(default_factory=BridgeConfig)

    # State
    _state: BridgeState = BridgeState.DISABLED
    _repl_bridge: Optional[REPLBridge] = None
    _sessions: dict[str, SessionInfo] = field(default_factory=dict)
    _current_session: Optional[SessionInfo] = None

    # Callbacks
    _on_state_change: Optional[Callable[[BridgeState], None]] = None
    _on_message: Optional[Callable[[BridgeMessage], None]] = None
    _on_event: Optional[Callable[[BridgeEvent], None]] = None

    # App state access
    _get_app_state: Optional[Callable[[], Any]] = None
    _set_app_state: Optional[Callable[[Callable], None]] = None

    @property
    def state(self) -> BridgeState:
        return self._state

    @property
    def is_enabled(self) -> bool:
        return self.config.enabled

    @property
    def is_connected(self) -> bool:
        return self._repl_bridge is not None and self._repl_bridge.is_connected

    @property
    def current_session(self) -> Optional[SessionInfo]:
        return self._current_session

    def initialize(
        self,
        get_app_state: Callable[[], Any],
        set_app_state: Callable[[Callable], None],
    ) -> None:
        """Initialize the bridge with app state access."""
        self._get_app_state = get_app_state
        self._set_app_state = set_app_state

    def set_on_state_change(self, callback: Callable[[BridgeState], None]) -> None:
        """Set state change callback."""
        self._on_state_change = callback

    def set_on_message(self, callback: Callable[[BridgeMessage], None]) -> None:
        """Set message callback."""
        self._on_message = callback

    def set_on_event(self, callback: Callable[[BridgeEvent], None]) -> None:
        """Set event callback."""
        self._on_event = callback

    async def enable(self) -> None:
        """Enable the bridge."""
        if self._state != BridgeState.DISABLED:
            return

        self._state = BridgeState.ENABLED
        self._notify_state_change()

        if self._get_app_state and self._set_app_state:
            # Create REPL bridge
            repl_config = REPLBridgeConfig(
                enabled=True,
                url=self.config.url,
                environment_id=self.config.environment_id,
                session_name=None,  # Will be set when connected
                outbound_only=self.config.outbound_only,
            )

            self._repl_bridge = REPLBridge(
                config=repl_config,
                get_app_state=self._get_app_state,
                set_app_state=self._set_app_state,
            )

            # Register event handlers
            self._repl_bridge.on_event(
                BridgeEventType.MESSAGE,
                self._handle_remote_message,
            )
            self._repl_bridge.on_event(
                BridgeEventType.TOOL_USE,
                self._handle_tool_use,
            )
            self._repl_bridge.on_event(
                BridgeEventType.ERROR,
                self._handle_error,
            )

            # Connect
            await self._repl_bridge.enable()
            self._state = BridgeState.CONNECTED
            self._notify_state_change()

    async def disable(self) -> None:
        """Disable the bridge."""
        if self._repl_bridge:
            await self._repl_bridge.disable()
            self._repl_bridge = None

        self._state = BridgeState.DISABLED
        self._current_session = None
        self._notify_state_change()

    async def send_message(self, message: BridgeMessage) -> None:
        """Send a message through the bridge."""
        if not self._repl_bridge:
            raise RuntimeError("Bridge not enabled")

        await self._repl_bridge.send_message(message)

    async def receive_message(self) -> BridgeMessage:
        """Receive a message from the bridge."""
        if not self._repl_bridge:
            raise RuntimeError("Bridge not enabled")

        return await self._repl_bridge.receive_message()

    async def create_session(self, name: Optional[str] = None) -> SessionInfo:
        """Create a new bridge session."""
        session = SessionInfo(
            id=self._generate_session_id(),
            name=name,
            created_at=self._current_time(),
            last_active=self._current_time(),
        )

        self._sessions[session.id] = session
        self._current_session = session

        # Emit event
        await self._emit_event(
            BridgeEventType.SESSION_START,
            {'session': session.__dict__},
        )

        return session

    async def end_session(self, session_id: str) -> None:
        """End a bridge session."""
        if session_id in self._sessions:
            session = self._sessions[session_id]
            session.status = 'ended'

            # Emit event
            await self._emit_event(
                BridgeEventType.SESSION_END,
                {'session_id': session_id},
            )

            if self._current_session and self._current_session.id == session_id:
                self._current_session = None

            del self._sessions[session_id]

    def get_sessions(self) -> list[SessionInfo]:
        """Get all active sessions."""
        return [
            s for s in self._sessions.values()
            if s.status == 'active'
        ]

    async def _handle_remote_message(self, message: BridgeMessage) -> None:
        """Handle a message from remote client."""
        # Forward to app state
        if self._on_message:
            self._on_message(message)

    async def _handle_tool_use(self, message: BridgeMessage) -> None:
        """Handle a tool use from remote."""
        # This would execute the tool locally
        pass

    async def _handle_error(self, message: BridgeMessage) -> None:
        """Handle an error from remote."""
        error = message.payload.get('error', 'Unknown error')
        # Log or handle the error

    async def _emit_event(self, event_type: BridgeEventType, data: dict) -> None:
        """Emit a bridge event."""
        event = BridgeEvent(type=event_type, data=data)

        if self._on_event:
            self._on_event(event)

    def _notify_state_change(self) -> None:
        """Notify state change."""
        if self._on_state_change:
            self._on_state_change(self._state)

    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        import secrets
        return secrets.token_hex(16)

    def _current_time(self) -> int:
        """Get current timestamp."""
        import time
        return int(time.time() * 1000)


# Export
__all__ = ['BridgeMain', 'BridgeConfig']