"""SDK Message Adapter."""
from typing import Any


class SDKMessageAdapter:
    """Adapter for SDK messages."""

    def __init__(self):
        self.handlers: dict[str, callable] = {}

    def register_handler(self, message_type: str, handler: callable) -> None:
        """Register a handler for a message type."""
        self.handlers[message_type] = handler

    def handle_message(self, message: dict) -> None:
        """Handle an SDK message."""
        message_type = message.get('type')
        handler = self.handlers.get(message_type)
        if handler:
            handler(message)

    def adapt_message(self, message: dict) -> dict:
        """Adapt a message to SDK format."""
        return message


__all__ = ['SDKMessageAdapter']