"""
REPL Bridge - Always-on remote control for Claude Code.
"""

import asyncio
import json
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Callable, Optional, Union

from ..cli.transports import WebSocketTransport, SSETransport
from .types import (
    BridgeConfig,
    BridgeMessage,
    BridgeState,
    BridgeEventType,
    BridgeMessageType,
)


@dataclass
class REPLBridgeConfig:
    """Configuration for REPL Bridge."""
    enabled: bool = False
    url: Optional[str] = None
    ws_url: Optional[str] = None
    sse_url: Optional[str] = None
    api_key: Optional[str] = None
    environment_id: Optional[str] = None
    session_name: Optional[str] = None
    outbound_only: bool = False
    explicit: bool = False  # True when activated via /remote-control command


class REPLBridge:
    """
    REPL Bridge provides always-on remote control capability.
    Allows remote clients to connect and control Claude Code sessions.
    """

    def __init__(
        self,
        config: REPLBridgeConfig,
        get_app_state: Callable[[], Any],
        set_app_state: Callable[[Callable], None],
    ):
        self.config = config
        self.get_app_state = get_app_state
        self.set_app_state = set_app_state

        self._state = BridgeState.DISABLED
        self._ws_transport: Optional[WebSocketTransport] = None
        self._sse_transport: Optional[SSETransport] = None

        self._session_id: Optional[str] = None
        self._environment_id: Optional[str] = None

        self._receive_queue: asyncio.Queue[BridgeMessage] = asyncio.Queue()
        self._event_handlers: dict[BridgeEventType, list[Callable]] = {}

        self._running = False
        self._receive_task: Optional[asyncio.Task] = None
        self._ping_task: Optional[asyncio.Task] = None

    @property
    def state(self) -> BridgeState:
        return self._state

    @property
    def is_connected(self) -> bool:
        return self._state == BridgeState.CONNECTED

    @property
    def session_id(self) -> Optional[str]:
        return self._session_id

    @property
    def environment_id(self) -> Optional[str]:
        return self._environment_id

    async def enable(self) -> None:
        """Enable the bridge."""
        if not self.config.enabled:
            return

        self._state = BridgeState.CONNECTING
        await self._connect()

    async def disable(self) -> None:
        """Disable the bridge."""
        await self._disconnect()
        self._state = BridgeState.DISABLED

    async def _connect(self) -> None:
        """Connect to bridge server."""
        try:
            ws_url = self.config.ws_url or self._build_ws_url()
            sse_url = self.config.sse_url or self._build_sse_url()

            headers = {}
            if self.config.api_key:
                headers['Authorization'] = f'Bearer {self.config.api_key}'

            # Connect SSE for receiving
            if sse_url:
                self._sse_transport = SSETransport(
                    url=sse_url,
                    headers=headers,
                    reconnect=True,
                )
                await self._sse_transport.connect()

            # Connect WebSocket for sending
            if ws_url:
                self._ws_transport = WebSocketTransport(
                    url=ws_url,
                    headers=headers,
                )
                await self._ws_transport.connect()

            # Create session
            await self._create_session()

            self._state = BridgeState.CONNECTED
            self._running = True

            # Start background tasks
            self._receive_task = asyncio.create_task(self._receive_loop())
            self._ping_task = asyncio.create_task(self._ping_loop())

        except Exception as e:
            self._state = BridgeState.ERROR
            raise

    async def _disconnect(self) -> None:
        """Disconnect from bridge server."""
        self._running = False

        # Cancel background tasks
        if self._ping_task:
            self._ping_task.cancel()
            try:
                await self._ping_task
            except asyncio.CancelledError:
                pass

        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        # Close transports
        if self._ws_transport:
            await self._ws_transport.disconnect()
            self._ws_transport = None

        if self._sse_transport:
            await self._sse_transport.disconnect()
            self._sse_transport = None

    async def send_message(self, message: BridgeMessage) -> None:
        """Send a message through the bridge."""
        if not self._ws_transport:
            raise RuntimeError("Bridge not connected")

        await self._ws_transport.send({
            'id': message.id,
            'type': message.type,
            'payload': message.payload,
            'timestamp': message.timestamp,
            'session_id': message.session_id or self._session_id,
        })

    async def receive_message(self) -> BridgeMessage:
        """Receive a message from the bridge."""
        return await self._receive_queue.get()

    def on_event(self, event_type: BridgeEventType, handler: Callable) -> None:
        """Register an event handler."""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)

    async def _receive_loop(self) -> None:
        """Background task to receive messages."""
        if not self._sse_transport:
            return

        try:
            async for data in self._sse_transport.receive():
                message = BridgeMessage(
                    id=data.get('id', ''),
                    type=data.get('type', ''),
                    payload=data.get('payload', {}),
                    timestamp=data.get('timestamp', 0),
                    session_id=data.get('session_id'),
                )

                # Queue the message
                await self._receive_queue.put(message)

                # Handle event
                await self._handle_message(message)

        except Exception:
            if self._running:
                # Try to reconnect
                self._state = BridgeState.RECONNECTING
                await self._reconnect()

    async def _handle_message(self, message: BridgeMessage) -> None:
        """Handle an incoming message."""
        # Dispatch to handlers
        event_type = BridgeEventType(message.type)
        handlers = self._event_handlers.get(event_type, [])

        for handler in handlers:
            try:
                await handler(message)
            except Exception:
                pass  # Log but don't crash

        # Handle specific message types
        if message.type == BridgeEventType.MESSAGE.value:
            await self._handle_user_message(message)
        elif message.type == BridgeEventType.TOOL_USE.value:
            await self._handle_tool_use(message)
        elif message.type == BridgeEventType.ERROR.value:
            await self._handle_error(message)

    async def _handle_user_message(self, message: BridgeMessage) -> None:
        """Handle a user message from remote."""
        # This would integrate with the query engine
        pass

    async def _handle_tool_use(self, message: BridgeMessage) -> None:
        """Handle a tool use from remote."""
        # Forward to local tool execution
        pass

    async def _handle_error(self, message: BridgeMessage) -> None:
        """Handle an error message."""
        error = message.payload.get('error', 'Unknown error')
        # Log the error
        print(f"Bridge error: {error}")

    async def _ping_loop(self) -> None:
        """Background task to send periodic pings."""
        while self._running:
            await asyncio.sleep(30)
            if self._ws_transport and self._ws_transport.is_connected:
                await self._ws_transport.send({
                    'type': BridgeMessageType.PING.value,
                })

    async def _reconnect(self) -> None:
        """Attempt to reconnect."""
        await self._disconnect()
        await asyncio.sleep(1)
        await self._connect()

    async def _create_session(self) -> None:
        """Create a new bridge session."""
        # Send session create request
        session_data = {
            'name': self.config.session_name or 'Python Session',
            'environment_id': self.config.environment_id,
        }

        if self._ws_transport:
            await self._ws_transport.send({
                'type': BridgeMessageType.SESSION_CREATE.value,
                'payload': session_data,
            })

    def _build_ws_url(self) -> str:
        """Build WebSocket URL from config."""
        base = self.config.url or 'wss://api.anthropic.com'
        env_id = self.config.environment_id or ''
        return f"{base}/bridge/ws/{env_id}"

    def _build_sse_url(self) -> str:
        """Build SSE URL from config."""
        base = self.config.url or 'https://api.anthropic.com'
        env_id = self.config.environment_id or ''
        return f"{base}/bridge/events/{env_id}"


__all__ = ['REPLBridge', 'REPLBridgeConfig']