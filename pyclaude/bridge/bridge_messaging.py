"""Bridge messaging - message handling for bridge."""

import json
import asyncio
from typing import Any, Callable, Optional, Dict
from dataclasses import dataclass
from enum import Enum

from .types import BridgeMessage, BridgeMessageType


class MessagePriority(str, Enum):
    """Message priority levels."""
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    CRITICAL = 'critical'


@dataclass
class QueuedMessage:
    """A queued message for transmission."""
    message: BridgeMessage
    priority: MessagePriority = MessagePriority.NORMAL
    retries: int = 0
    max_retries: int = 3


class BridgeMessaging:
    """Bridge messaging handler."""

    def __init__(self):
        self._message_queue: list[QueuedMessage] = []
        self._handlers: Dict[str, Callable] = {}
        self._send_callback: Optional[Callable[[BridgeMessage], Any]] = None

    def set_send_callback(self, callback: Callable[[BridgeMessage], Any]) -> None:
        """Set the send callback."""
        self._send_callback = callback

    def register_handler(self, message_type: str, handler: Callable) -> None:
        """Register a message handler."""
        self._handlers[message_type] = handler

    async def handle_message(self, message: BridgeMessage) -> None:
        """Handle an incoming message."""
        handler = self._handlers.get(message.type)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                # Log error but don't crash
                print(f'Error handling message: {e}')

    async def send_message(
        self,
        message_type: str,
        payload: dict,
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> None:
        """Send a message."""
        message = BridgeMessage(
            id='',
            type=message_type,
            payload=payload,
        )

        if self._send_callback:
            await self._send_callback(message)
        else:
            # Queue for later
            self._message_queue.append(QueuedMessage(message, priority))

    async def send_with_retry(
        self,
        message: BridgeMessage,
        max_retries: int = 3,
    ) -> bool:
        """Send a message with retry on failure."""
        for attempt in range(max_retries):
            try:
                if self._send_callback:
                    await self._send_callback(message)
                    return True
            except Exception as e:
                print(f'Send attempt {attempt + 1} failed: {e}')
                await asyncio.sleep(0.5 * (attempt + 1))

        return False

    def get_queue_size(self) -> int:
        """Get the message queue size."""
        return len(self._message_queue)

    def clear_queue(self) -> None:
        """Clear the message queue."""
        self._message_queue.clear()


# Global messaging instance
_messaging = BridgeMessaging()


def get_bridge_messaging() -> BridgeMessaging:
    """Get the global bridge messaging instance."""
    return _messaging


__all__ = [
    'BridgeMessaging',
    'QueuedMessage',
    'MessagePriority',
    'get_bridge_messaging',
]