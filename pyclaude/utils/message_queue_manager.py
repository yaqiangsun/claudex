"""
Message queue manager utility.
"""
from typing import Any, List
from collections import deque

class MessageQueueManager:
    def __init__(self):
        self._queue = deque()

    def enqueue(self, message: Any) -> None:
        self._queue.append(message)

    def dequeue(self) -> Any:
        if self._queue:
            return self._queue.popleft()
        return None

    def size(self) -> int:
        return len(self._queue)

_queue = MessageQueueManager()

def get_message_queue() -> MessageQueueManager:
    return _queue

__all__ = ['MessageQueueManager', 'get_message_queue']