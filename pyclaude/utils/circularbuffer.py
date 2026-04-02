"""
Circular buffer utility.

A fixed-size circular buffer that automatically evicts the oldest items
when the buffer is full.
"""

from typing import Generic, TypeVar, List

T = TypeVar('T')


class CircularBuffer(Generic[T]):
    """A fixed-size circular buffer that automatically evicts the oldest items."""

    def __init__(self, capacity: int):
        self._capacity = capacity
        self._buffer: List[T] = []
        self._head = 0
        self._size = 0

    def add(self, item: T) -> None:
        """Add an item to the buffer."""
        if self._size < self._capacity:
            self._buffer.append(item)
            self._size += 1
        else:
            self._buffer[self._head] = item
            self._head = (self._head + 1) % self._capacity

    def add_all(self, items: List[T]) -> None:
        """Add multiple items to the buffer."""
        for item in items:
            self.add(item)

    def get_recent(self, count: int) -> List[T]:
        """Get the most recent N items."""
        if self._size == 0:
            return []
        available = min(count, self._size)
        start = 0 if self._size < self._capacity else self._head
        result = []
        for i in range(available):
            idx = (start + self._size - available + i) % self._capacity
            if idx < len(self._buffer):
                result.append(self._buffer[idx])
        return result

    def to_array(self) -> List[T]:
        """Get all items in order from oldest to newest."""
        if self._size == 0:
            return []
        start = 0 if self._size < self._capacity else self._head
        result = []
        for i in range(self._size):
            idx = (start + i) % self._capacity
            if idx < len(self._buffer):
                result.append(self._buffer[idx])
        return result

    def clear(self) -> None:
        """Clear all items."""
        self._buffer = []
        self._head = 0
        self._size = 0

    def length(self) -> int:
        """Get the current number of items."""
        return self._size


__all__ = ['CircularBuffer']