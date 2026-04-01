"""
Hybrid transport - combines WebSocket and SSE.
"""

import asyncio
import json
from typing import Any, AsyncGenerator, Optional, Union

from .transport import Transport, TransportState, TransportError
from .websocket import WebSocketTransport
from .sse import SSETransport


class HybridTransport(Transport):
    """
    Hybrid transport that uses WebSocket for sending and SSE for receiving.

    This is useful when:
    - Server requires SSE for receiving events (long-lived connections)
    - WebSocket provides better latency for sending
    """

    def __init__(
        self,
        ws_url: Optional[str] = None,
        sse_url: Optional[str] = None,
        ws_headers: Optional[dict] = None,
        sse_headers: Optional[dict] = None,
    ):
        # Use same URL for both if only one provided
        self._ws_url = ws_url
        self._sse_url = sse_url or ws_url
        self._ws_headers = ws_headers or {}
        self._sse_headers = sse_headers or {}

        super().__init__(url=ws_url or sse_url)

        self._ws_transport: Optional[WebSocketTransport] = None
        self._sse_transport: Optional[SSETransport] = None
        self._receive_task: Optional[asyncio.Task] = None
        self._event_queue: asyncio.Queue[dict] = asyncio.Queue()
        self._close_event: asyncio.Event = asyncio.Event()

    async def connect(self) -> None:
        """Connect both WebSocket and SSE transports."""
        self._state = TransportState.CONNECTING

        try:
            # Connect WebSocket (for sending)
            if self._ws_url:
                self._ws_transport = WebSocketTransport(
                    url=self._ws_url,
                    headers=self._ws_headers,
                )
                await self._ws_transport.connect()

            # Connect SSE (for receiving)
            if self._sse_url:
                self._sse_transport = SSETransport(
                    url=self._sse_url,
                    headers=self._sse_headers,
                    reconnect=True,
                )
                await self._sse_transport.connect()

            self._state = TransportState.CONNECTED
            self.reset_reconnect()

            # Start receiving from SSE
            if self._sse_transport:
                self._receive_task = asyncio.create_task(self._receive_loop())

        except Exception as e:
            self._state = TransportState.ERROR
            await self.disconnect()
            raise TransportError(
                f"Failed to connect: {str(e)}",
                code="CONNECTION_FAILED"
            )

    async def disconnect(self) -> None:
        """Disconnect both transports."""
        self._close_event.set()

        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        if self._ws_transport:
            await self._ws_transport.disconnect()
            self._ws_transport = None

        if self._sse_transport:
            await self._sse_transport.disconnect()
            self._sse_transport = None

        self._state = TransportState.DISCONNECTED

    async def send(self, data: dict) -> None:
        """Send data via WebSocket."""
        if not self._ws_transport:
            raise TransportError(
                "WebSocket not connected",
                code="NOT_CONNECTED"
            )

        await self._ws_transport.send(data)

    async def receive(self) -> AsyncGenerator[dict, None]:
        """Receive events from SSE."""
        while not self._close_event.is_set():
            try:
                event = await asyncio.wait_for(
                    self._event_queue.get(),
                    timeout=1.0
                )
                yield event
            except asyncio.TimeoutError:
                continue

    async def _receive_loop(self) -> None:
        """Background task to receive from SSE."""
        if not self._sse_transport:
            return

        try:
            async for event in self._sse_transport.receive():
                if self._close_event.is_set():
                    break
                await self._event_queue.put(event)
        except Exception:
            # Try to reconnect
            if await self._sse_transport._try_reconnect():
                await self._receive_loop()
            else:
                self._state = TransportState.ERROR


class SerialBatchEventUploader(Transport):
    """
    Uploader that serializes events and uploads in batches.
    """

    def __init__(
        self,
        upload_url: str,
        batch_size: int = 10,
        flush_interval: float = 5.0,
    ):
        super().__init__(url=upload_url)
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self._queue: list[dict] = []
        self._flush_task: Optional[asyncio.Task] = None
        self._close_event: asyncio.Event = asyncio.Event()
        self._client = None

    async def connect(self) -> None:
        """Initialize the uploader."""
        try:
            import httpx
            self._client = httpx.AsyncClient()
            self._state = TransportState.CONNECTED

            # Start periodic flush
            self._flush_task = asyncio.create_task(self._flush_loop())

        except Exception as e:
            self._state = TransportState.ERROR
            raise TransportError(f"Failed to connect: {str(e)}")

    async def disconnect(self) -> None:
        """Disconnect and flush remaining events."""
        self._close_event.set()

        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass

        # Flush remaining
        await self._flush()

        if self._client:
            await self._client.aclose()
            self._client = None

        self._state = TransportState.DISCONNECTED

    async def send(self, data: dict) -> None:
        """Queue event for batch upload."""
        self._queue.append(data)

        if len(self._queue) >= self.batch_size:
            await self._flush()

    async def receive(self) -> AsyncGenerator[dict, None]:
        """Not used for uploader."""
        while not self._close_event.is_set():
            await asyncio.sleep(1)

    async def _flush(self) -> None:
        """Upload queued events."""
        if not self._queue or not self._client:
            return

        events = list(self._queue)
        self._queue.clear()

        try:
            await self._client.post(
                self.url,
                json={'events': events},
                timeout=30.0,
            )
        except Exception:
            # Re-queue on failure
            self._queue.extend(events)

    async def _flush_loop(self) -> None:
        """Periodic flush task."""
        while not self._close_event.is_set():
            await asyncio.sleep(self.flush_interval)
            await self._flush()


class WorkerStateUploader(SerialBatchEventUploader):
    """Uploader for worker state updates."""

    def __init__(self, upload_url: str):
        super().__init__(
            upload_url=upload_url,
            batch_size=1,
            flush_interval=1.0,
        )

    async def send_state(self, state: dict) -> None:
        """Send worker state."""
        await self.send({'type': 'state', 'state': state})


__all__ = [
    'HybridTransport',
    'SerialBatchEventUploader',
    'WorkerStateUploader',
]