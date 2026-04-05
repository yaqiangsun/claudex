"""History management for conversation sessions."""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    """A conversation message."""
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class History:
    """Conversation history."""
    messages: List[Message] = field(default_factory=list)
    session_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """Add a message to history."""
        msg = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(msg)

    def get_messages(self) -> List[Message]:
        """Get all messages."""
        return self.messages.copy()

    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()

    def count(self) -> int:
        """Get message count."""
        return len(self.messages)


# Global history instance
_history = History()


def get_history() -> History:
    """Get global history instance."""
    return _history


def add_user_message(content: str) -> None:
    """Add a user message."""
    _history.add_message("user", content)


def add_assistant_message(content: str) -> None:
    """Add an assistant message."""
    _history.add_message("assistant", content)


def add_system_message(content: str) -> None:
    """Add a system message."""
    _history.add_message("system", content)


def clear_history() -> None:
    """Clear conversation history."""
    _history.clear()


__all__ = [
    'Message',
    'History',
    'get_history',
    'add_user_message',
    'add_assistant_message',
    'add_system_message',
    'clear_history',
]