"""
Structured I/O for Claude Code communication.
"""

import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncGenerator, Optional


class EventType(str, Enum):
    """Event types for structured I/O."""
    MESSAGE = 'message'
    TOOL_USE = 'tool_use'
    TOOL_RESULT = 'tool_result'
    ERROR = 'error'
    COMPLETION = 'completion'
    PROGRESS = 'progress'
    SYSTEM = 'system'


@dataclass
class Event:
    """Structured event."""
    type: EventType
    data: dict = field(default_factory=dict)
    timestamp: int = 0

    def __post_init__(self):
        if self.timestamp == 0:
            import time
            self.timestamp = int(time.time() * 1000)

    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps({
            'type': self.type.value,
            'data': self.data,
            'timestamp': self.timestamp,
        })


class StructuredIO(ABC):
    """Abstract base for structured I/O handlers."""

    @abstractmethod
    async def send_message(self, message: dict) -> None:
        """Send a message event."""
        pass

    @abstractmethod
    async def send_tool_use(self, tool_use: dict) -> None:
        """Send a tool use event."""
        pass

    @abstractmethod
    async def send_tool_result(self, result: dict) -> None:
        """Send a tool result event."""
        pass

    @abstractmethod
    async def send_error(self, error: str, details: Optional[dict] = None) -> None:
        """Send an error event."""
        pass

    @abstractmethod
    async def send_completion(self, message: dict) -> None:
        """Send a completion event."""
        pass

    @abstractmethod
    async def send_progress(self, progress: dict) -> None:
        """Send a progress event."""
        pass

    @abstractmethod
    async def send_system(self, message: str) -> None:
        """Send a system message."""
        pass


class ConsoleStructuredIO(StructuredIO):
    """Structured I/O that outputs to console."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        from .print import print, print_error, print_info
        self._print = print
        self._print_error = print_error
        self._print_info = print_info

    async def send_message(self, message: dict) -> None:
        """Send a message event."""
        content = message.get('content', [])
        for block in content:
            if block.get('type') == 'text':
                self._print(block.get('text', ''))

    async def send_tool_use(self, tool_use: dict) -> None:
        """Send a tool use event."""
        name = tool_use.get('name', 'unknown')
        input_data = tool_use.get('input', {})
        self._print_info(f"[Using tool: {name}]")
        if self.verbose:
            self._print(f"  Input: {json.dumps(input_data)}")

    async def send_tool_result(self, result: dict) -> None:
        """Send a tool result event."""
        content = result.get('content', '')
        is_error = result.get('is_error', False)
        if is_error:
            self._print_error(content)
        else:
            self._print(content[:500] if len(content) > 500 else content)

    async def send_error(self, error: str, details: Optional[dict] = None) -> None:
        """Send an error event."""
        self._print_error(error)
        if self.verbose and details:
            self._print(f"  Details: {json.dumps(details)}")

    async def send_completion(self, message: dict) -> None:
        """Send a completion event."""
        stop_reason = message.get('stop_reason', 'end_turn')
        self._print_info(f"[Completed: {stop_reason}]")

    async def send_progress(self, progress: dict) -> None:
        """Send a progress event."""
        if self.verbose:
            tool_name = progress.get('tool_name', 'unknown')
            self._print_info(f"[Progress: {tool_name}]")

    async def send_system(self, message: str) -> None:
        """Send a system message."""
        self._print(f"[System] {message}")


class JSONStructuredIO(StructuredIO):
    """Structured I/O that outputs JSON lines."""

    def __init__(self, output_file=None):
        self.output_file = output_file

    async def _send(self, event: Event) -> None:
        """Send an event."""
        line = event.to_json()
        if self.output_file:
            self.output_file.write(line + '\n')
            self.output_file.flush()
        else:
            print(line)

    async def send_message(self, message: dict) -> None:
        """Send a message event."""
        await self._send(Event(type=EventType.MESSAGE, data=message))

    async def send_tool_use(self, tool_use: dict) -> None:
        """Send a tool use event."""
        await self._send(Event(type=EventType.TOOL_USE, data=tool_use))

    async def send_tool_result(self, result: dict) -> None:
        """Send a tool result event."""
        await self._send(Event(type=EventType.TOOL_RESULT, data=result))

    async def send_error(self, error: str, details: Optional[dict] = None) -> None:
        """Send an error event."""
        await self._send(Event(
            type=EventType.ERROR,
            data={'error': error, 'details': details or {}}
        ))

    async def send_completion(self, message: dict) -> None:
        """Send a completion event."""
        await self._send(Event(type=EventType.COMPLETION, data=message))

    async def send_progress(self, progress: dict) -> None:
        """Send a progress event."""
        await self._send(Event(type=EventType.PROGRESS, data=progress))

    async def send_system(self, message: str) -> None:
        """Send a system message."""
        await self._send(Event(
            type=EventType.SYSTEM,
            data={'message': message}
        ))


def create_structured_io(
    format: str = 'console',
    output_file=None,
) -> StructuredIO:
    """Create a structured I/O handler."""
    if format == 'console':
        return ConsoleStructuredIO(verbose=False)
    elif format == 'json':
        return JSONStructuredIO(output_file=output_file)
    else:
        raise ValueError(f"Unknown format: {format}")


# NDJSON safe stringification
def ndjson_safe_stringify(obj: Any) -> str:
    """
    Safely stringify an object for NDJSON output.
    Replaces newlines and control characters.
    """
    s = json.dumps(obj)
    # Replace newlines and control characters
    s = s.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    return s


__all__ = [
    'EventType',
    'Event',
    'StructuredIO',
    'ConsoleStructuredIO',
    'JSONStructuredIO',
    'create_structured_io',
    'ndjson_safe_stringify',
]