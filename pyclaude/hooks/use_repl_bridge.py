"""Hook for REPL bridge communication."""


class ReplBridge:
    """Manages REPL bridge communication."""

    def __init__(self):
        self._connected = False
        self._messages = []

    def connect(self) -> bool:
        """Connect to REPL bridge."""
        self._connected = True
        return True

    def disconnect(self) -> None:
        """Disconnect from REPL bridge."""
        self._connected = False

    def is_connected(self) -> bool:
        """Check if connected."""
        return self._connected

    def send(self, message: dict) -> None:
        """Send a message through the bridge."""
        if self._connected:
            self._messages.append(message)

    def receive(self) -> list:
        """Receive messages from the bridge."""
        messages = self._messages.copy()
        self._messages.clear()
        return messages


__all__ = ['ReplBridge']