"""
WebSocket transport implementation.
"""

import asyncio
import json
from typing import Any, AsyncGenerator, Optional, Union

try:
    import websockets
    from websockets import WebSocketClientProtocol
except ImportError:
    websockets = None
    WebSocketClientProtocol = Any

from .transport import Transport, TransportState, TransportError


class WebSocketTransport(Transport):
    """WebSocket-based transport."""

    def __init__(
        self,
        url: str,
        headers: Optional[dict] = None,
        ping_interval: int = 30,
    ):
        super().__init__(url)
        self.headers = headers or {}
        self.ping_interval = ping_interval
        self._ws: Optional[WebSocketClientProtocol] = None
        self._receive_task: Optional[asyncio.Task] = None
        self._queue: asyncio.Queue[dict] = asyncio.Queue()
        self._close_event: asyncio.Event = asyncio.Event()

    async def connect(self) -> None:
        """Connect to WebSocket server."""
        if websockets is None:
            raise TransportError(
                "websockets library not installed",
                code="MISSING_DEPENDENCY"
            )

        self._state = TransportState.CONNECTING

        try:
            self._ws = await websockets.connect(
                self.url,
                extra_headers=self.headers,
                ping_interval=self.ping_interval,
            )
            self._state = TransportState.CONNECTED
            self.reset_reconnect()

            # Start receive loop
            self._receive_task = asyncio.create_task(self._receive_loop())

        except Exception as e:
            self._state = TransportState.ERROR
            raise TransportError(
                f"Failed to connect: {str(e)}",
                code="CONNECTION_FAILED"
            )

    async def disconnect(self) -> None:
        """Disconnect from WebSocket server."""
        self._close_event.set()

        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        if self._ws:
            await self._ws.close()
            self._ws = None

        self._state = TransportState.DISCONNECTED

    async def send(self, data: dict) -> None:
        """Send data through WebSocket."""
        if not self._ws or self._state != TransportState.CONNECTED:
            raise TransportError(
                "Not connected",
                code="NOT_CONNECTED"
            )

        try:
            message = json.dumps(data)
            await self._ws.send(message)
        except Exception as e:
            raise TransportError(
                f"Failed to send: {str(e)}",
                code="SEND_FAILED"
            )

    async def receive(self) -> AsyncGenerator[dict, None]:
        """Receive data from WebSocket."""
        while not self._close_event.is_set():
            try:
                data = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                yield data
            except asyncio.TimeoutError:
                continue

    async def _receive_loop(self) -> None:
        """Background task to receive messages."""
        try:
            async for message in self._ws:
                if self._close_event.is_set():
                    break

                try:
                    data = json.loads(message)
                    self._queue.put_nowait(data)
                except json.JSONDecodeError:
                    # Handle non-JSON messages
                    self._queue.put_nowait({'raw': message})

        except websockets.exceptions.ConnectionClosed as e:
            self._state = TransportState.DISCONNECTED
            # Try to reconnect
            if await self._try_reconnect():
                # Reconnected, continue receiving
                pass
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self._state = TransportState.ERROR

    async def ping(self) -> bool:
        """Send a ping and return True if pong received."""
        if not self._ws:
            return False
        try:
            await self._ws.ping()
            return True
        except Exception:
            return False


class WebSocketServerTransport(Transport):
    """WebSocket server-side transport (for incoming connections)."""

    def __init__(self, ws: WebSocketClientProtocol):
        super().__init__(url=None)
        self._ws = ws
        self._queue: asyncio.Queue[dict] = asyncio.Queue()
        self._close_event: asyncio.Event = asyncio.Event()

    async def connect(self) -> None:
        self._state = TransportState.CONNECTED

    async def disconnect(self) -> None:
        self._close_event.set()
        await self._ws.close()
        self._state = TransportState.DISCONNECTED

    async def send(self, data: dict) -> None:
        if not self._ws:
            raise TransportError("Not connected", code="NOT_CONNECTED")
        await self._ws.send(json.dumps(data))

    async def receive(self) -> AsyncGenerator[dict, None]:
        while not self._close_event.is_set():
            try:
                message = await asyncio.wait_for(self._ws.recv(), timeout=1.0)
                try:
                    data = json.loads(message)
                    yield data
                except json.JSONDecodeError:
                    yield {'raw': message}
            except asyncio.TimeoutError:
                continue
            except websockets.exceptions.ConnectionClosed:
                break


__all__ = ['WebSocketTransport', 'WebSocketServerTransport']