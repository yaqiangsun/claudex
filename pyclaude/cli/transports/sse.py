"""
Server-Sent Events (SSE) transport implementation.
"""

import asyncio
import json
import re
from typing import Any, AsyncGenerator, Optional, Union

try:
    import httpx
except ImportError:
    httpx = None

from .transport import Transport, TransportState, TransportError


class SSETransport(Transport):
    """SSE-based transport for receiving server events."""

    def __init__(
        self,
        url: str,
        method: str = 'GET',
        headers: Optional[dict] = None,
        body: Optional[dict] = None,
        reconnect: bool = True,
    ):
        super().__init__(url)
        self.method = method
        self.headers = headers or {}
        self.body = body or {}
        self.reconnect = reconnect
        self._client: Optional[httpx.AsyncClient] = None
        self._event_queue: asyncio.Queue[dict] = asyncio.Queue()
        self._close_event: asyncio.Event = asyncio.Event()
        self._last_event_id: Optional[str] = None

    async def connect(self) -> None:
        """Connect and start receiving SSE events."""
        if httpx is None:
            raise TransportError(
                "httpx library not installed",
                code="MISSING_DEPENDENCY"
            )

        self._state = TransportState.CONNECTING

        try:
            self._client = httpx.AsyncClient(
                headers=self.headers,
                timeout=httpx.Timeout(30.0, connect=10.0),
            )

            # Make request
            if self.method == 'GET':
                response = await self._client.get(self.url)
            elif self.method == 'POST':
                response = await self._client.post(self.url, json=self.body)
            else:
                raise TransportError(f"Unsupported method: {self.method}")

            response.raise_for_status()

            self._state = TransportState.CONNECTED
            self.reset_reconnect()

            # Start processing SSE stream
            asyncio.create_task(self._process_stream(response))

        except Exception as e:
            self._state = TransportState.ERROR
            raise TransportError(
                f"Failed to connect: {str(e)}",
                code="CONNECTION_FAILED"
            )

    async def disconnect(self) -> None:
        """Disconnect from SSE endpoint."""
        self._close_event.set()

        if self._client:
            await self._client.aclose()
            self._client = None

        self._state = TransportState.DISCONNECTED

    async def send(self, data: dict) -> None:
        """Send data (typically POST to endpoint)."""
        if not self._client:
            raise TransportError("Not connected", code="NOT_CONNECTED")

        try:
            response = await self._client.post(self.url, json=data)
            response.raise_for_status()
        except Exception as e:
            raise TransportError(
                f"Failed to send: {str(e)}",
                code="SEND_FAILED"
            )

    async def receive(self) -> AsyncGenerator[dict, None]:
        """Receive SSE events."""
        while not self._close_event.is_set():
            try:
                event = await asyncio.wait_for(
                    self._event_queue.get(),
                    timeout=1.0
                )
                yield event
            except asyncio.TimeoutError:
                continue

    async def _process_stream(self, response: httpx.Response) -> None:
        """Process the SSE stream."""
        try:
            async for line in response.aiter_lines():
                if self._close_event.is_set():
                    break

                if not line.strip():
                    continue

                # Parse SSE format: "event: type" or "data: json"
                event = self._parse_sse_line(line)
                if event:
                    await self._event_queue.put(event)

        except httpx.ConnectError:
            if self.reconnect:
                await self._try_reconnect()
        except Exception:
            self._state = TransportState.ERROR

    def _parse_sse_line(self, line: str) -> Optional[dict]:
        """Parse a single SSE line."""
        # Handle comment lines
        if line.startswith(':'):
            return None

        # Parse event type
        if line.startswith('event:'):
            return None  # Event type handled separately

        # Parse data
        if line.startswith('data:'):
            data = line[5:].strip()
            if not data:
                return None

            # Try to parse as JSON
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                # Return as raw text
                return {'type': 'message', 'data': data}

        return None


class SSEReconnectTransport(SSETransport):
    """SSE transport with automatic reconnection."""

    def __init__(self, *args, max_retries: int = 10, retry_delay: float = 1.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._retry_count = 0

    async def _try_reconnect(self) -> bool:
        """Override to add custom reconnection logic."""
        if self._retry_count >= self.max_retries:
            return False

        self._state = TransportState.RECONNECTING
        self._retry_count += 1

        delay = self.retry_delay * (2 ** min(self._retry_count - 1, 5))
        await asyncio.sleep(min(delay, 60))  # Cap at 60 seconds

        try:
            await self.connect()
            self._retry_count = 0
            return True
        except Exception:
            return False


__all__ = ['SSETransport', 'SSEReconnectTransport']