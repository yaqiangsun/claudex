"""Bridge API - API for bridge operations."""

from typing import Any, Callable, Optional
from dataclasses import dataclass

from .types import BridgeConfig, BridgeState, BridgeMessage


@dataclass
class BridgeAPI:
    """Bridge API for external communication."""

    _send_message: Optional[Callable[[BridgeMessage], None]] = None
    _on_message: Optional[Callable[[BridgeMessage], None]] = None

    def set_send_message(self, callback: Callable[[BridgeMessage], None]) -> None:
        """Set the message sender callback."""
        self._send_message = callback

    def set_on_message(self, callback: Callable[[BridgeMessage], None]) -> None:
        """Set the message handler callback."""
        self._on_message = callback

    async def send(self, message: BridgeMessage) -> None:
        """Send a message through the bridge."""
        if self._send_message:
            self._send_message(message)

    async def broadcast(self, message_type: str, payload: dict) -> None:
        """Broadcast a message to all connected clients."""
        message = BridgeMessage(
            id='',
            type=message_type,
            payload=payload,
        )
        await self.send(message)

    async def send_to_session(self, session_id: str, message: BridgeMessage) -> None:
        """Send a message to a specific session."""
        message.session_id = session_id
        await self.send(message)


# Global bridge API instance
_bridge_api = BridgeAPI()


def get_bridge_api() -> BridgeAPI:
    """Get the global bridge API instance."""
    return _bridge_api


__all__ = ['BridgeAPI', 'get_bridge_api']