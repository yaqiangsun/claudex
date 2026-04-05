"""Agent SDK types for Claude Code."""
from typing import Any, Dict, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum


class MessageRole(str, Enum):
    """Message role types."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """A conversation message."""
    role: MessageRole
    content: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ToolResult:
    """Result from a tool call."""
    success: bool
    result: Any = None
    error: Optional[str] = None


@dataclass
class SessionInfo:
    """Session information."""
    id: str
    created_at: int = 0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ToolAnnotations:
    """Tool annotations."""
    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        read_only_hint: bool = False,
    ):
        self.title = title
        self.description = description
        self.read_only_hint = read_only_hint


# Type aliases
CallToolResult = ToolResult
SDKMessage = Message
SDKUserMessage = Message
SDKResultMessage = Message


__all__ = [
    'MessageRole',
    'Message',
    'ToolResult',
    'SessionInfo',
    'ToolAnnotations',
    'CallToolResult',
    'SDKMessage',
    'SDKUserMessage',
    'SDKResultMessage',
]