"""
Input buffer hook - manages input history for undo functionality.

Python adaptation.
"""

from typing import Any, Dict, Callable, Optional
from dataclasses import dataclass, field
import time


@dataclass
class BufferEntry:
    """A single buffer entry."""
    text: str
    cursor_offset: int
    pasted_contents: Dict[int, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class InputBufferState:
    """State for input buffer management."""

    def __init__(self, max_buffer_size: int = 100, debounce_ms: int = 300):
        self.max_buffer_size = max_buffer_size
        self.debounce_ms = debounce_ms
        self.buffer: list[BufferEntry] = []
        self.current_index: int = -1
        self.last_push_time: float = 0
        self.pending_push: Optional[Any] = None  # Timer handle
        self._subscribers: list[Callable] = []

    def push_to_buffer(
        self,
        text: str,
        cursor_offset: int,
        pasted_contents: Optional[Dict[int, Any]] = None,
    ) -> None:
        """Push new text to the buffer."""
        now = time.time() * 1000  # ms

        # Clear any pending push
        if self.pending_push:
            # In Python we'd cancel the timer here
            self.pending_push = None

        # Debounce rapid changes
        if now - self.last_push_time < self.debounce_ms:
            # Schedule a delayed push
            self.pending_push = (text, cursor_offset, pasted_contents or {})
            return

        self.last_push_time = now

        # If we're not at the end of the buffer, truncate
        new_buffer = (
            self.buffer[: self.current_index + 1]
            if self.current_index >= 0
            else self.buffer
        )

        # Don't add if it's the same as the last entry
        last_entry = new_buffer[-1] if new_buffer else None
        if last_entry and last_entry.text == text:
            return

        # Add new entry
        new_entry = BufferEntry(
            text=text,
            cursor_offset=cursor_offset,
            pasted_contents=pasted_contents or {},
            timestamp=now,
        )
        new_buffer.append(new_entry)

        # Limit buffer size
        if len(new_buffer) > self.max_buffer_size:
            new_buffer = new_buffer[-self.max_buffer_size :]

        self.buffer = new_buffer

        # Update current index
        new_index = (
            self.current_index + 1 if self.current_index >= 0 else len(self.buffer) - 1
        )
        self.current_index = min(new_index, self.max_buffer_size - 1)

        self._notify_subscribers()

    def undo(self) -> Optional[BufferEntry]:
        """Undo and return the previous entry."""
        if self.current_index < 0 or len(self.buffer) == 0:
            return None

        target_index = max(0, self.current_index - 1)
        entry = self.buffer[target_index]

        if entry:
            self.current_index = target_index

        return entry

    def clear_buffer(self) -> None:
        """Clear the entire buffer."""
        self.buffer = []
        self.current_index = -1
        self.last_push_time = 0
        if self.pending_push:
            self.pending_push = None
        self._notify_subscribers()

    @property
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self.current_index > 0 and len(self.buffer) > 1

    def subscribe(self, callback: Callable) -> Callable:
        """Subscribe to buffer changes."""
        self._subscribers.append(callback)

        def unsubscribe():
            self._subscribers.remove(callback)

        return unsubscribe

    def _notify_subscribers(self) -> None:
        """Notify all subscribers of changes."""
        for callback in self._subscribers:
            callback()


# Global state storage
_input_buffer_state: Optional[InputBufferState] = None


def use_input_buffer(
    max_buffer_size: int = 100,
    debounce_ms: int = 300,
) -> Dict[str, Any]:
    """Hook that manages input buffer for undo functionality.

    Args:
        max_buffer_size: Maximum number of entries to keep
        debounce_ms: Debounce time in milliseconds

    Returns:
        Dictionary with push_to_buffer, undo, canUndo, clearBuffer functions
    """
    global _input_buffer_state

    if _input_buffer_state is None:
        _input_buffer_state = InputBufferState(max_buffer_size, debounce_ms)

    return {
        "push_to_buffer": _input_buffer_state.push_to_buffer,
        "undo": _input_buffer_state.undo,
        "can_undo": _input_buffer_state.can_undo,
        "clear_buffer": _input_buffer_state.clear_buffer,
    }


__all__ = ["use_input_buffer", "BufferEntry", "InputBufferState"]