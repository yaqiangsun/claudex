"""Hook for arrow key history navigation."""
from typing import List, Optional, Any


class ArrowKeyHistory:
    """Manages command history navigation with arrow keys."""

    def __init__(self, history: Optional[List[str]] = None):
        self._history = history or []
        self._position = len(self._history)

    def navigate_up(self) -> Optional[str]:
        """Navigate to previous history item."""
        if self._position > 0:
            self._position -= 1
            return self._history[self._position]
        return None

    def navigate_down(self) -> Optional[str]:
        """Navigate to next history item."""
        if self._position < len(self._history) - 1:
            self._position += 1
            return self._history[self._position]
        self._position = len(self._history)
        return ""

    def reset(self) -> None:
        """Reset position to end of history."""
        self._position = len(self._history)


__all__ = ['ArrowKeyHistory']