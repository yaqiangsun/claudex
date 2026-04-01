"""
Base transport interface.
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncGenerator, Optional


class TransportState(str, Enum):
    """Transport connection state."""
    DISCONNECTED = 'disconnected'
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    RECONNECTING = 'reconnecting'
    ERROR = 'error'


@dataclass
class TransportError(Exception):
    """Transport error."""
    message: str
    code: Optional[str] = None
    details: Optional[dict] = None

    def __init__(self, message: str, code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class Transport(ABC):
    """Abstract base class for transports."""

    def __init__(self, url: Optional[str] = None):
        self.url = url
        self._state = TransportState.DISCONNECTED
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = 5
        self._reconnect_delay = 1.0

    @property
    def state(self) -> TransportState:
        """Get connection state."""
        return self._state

    @property
    def is_connected(self) -> bool:
        """Check if connected."""
        return self._state == TransportState.CONNECTED

    @abstractmethod
    async def connect(self) -> None:
        """Connect to the transport."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the transport."""
        pass

    @abstractmethod
    async def send(self, data: dict) -> None:
        """Send data through the transport."""
        pass

    @abstractmethod
    async def receive(self) -> AsyncGenerator[dict, None]:
        """Receive data from the transport."""
        pass

    async def _try_reconnect(self) -> bool:
        """Attempt to reconnect."""
        if self._reconnect_attempts >= self._max_reconnect_attempts:
            return False

        self._state = TransportState.RECONNECTING
        self._reconnect_attempts += 1

        delay = self._reconnect_delay * (2 ** (self._reconnect_attempts - 1))
        await asyncio.sleep(min(delay, 30))  # Cap at 30 seconds

        try:
            await self.connect()
            self._reconnect_attempts = 0
            return True
        except Exception:
            return False

    def reset_reconnect(self) -> None:
        """Reset reconnect attempts."""
        self._reconnect_attempts = 0


class NullTransport(Transport):
    """Null transport for testing."""

    def __init__(self):
        super().__init__(url=None)
        self._queue: asyncio.Queue[dict] = asyncio.Queue()

    async def connect(self) -> None:
        self._state = TransportState.CONNECTED

    async def disconnect(self) -> None:
        self._state = TransportState.DISCONNECTED

    async def send(self, data: dict) -> None:
        pass

    async def receive(self) -> AsyncGenerator[dict, None]:
        while True:
            try:
                data = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                yield data
            except asyncio.TimeoutError:
                continue

    def put(self, data: dict) -> None:
        """Put data into the queue (for testing)."""
        self._queue.put_nowait(data)


__all__ = ['Transport', 'TransportState', 'TransportError', 'NullTransport']