"""Hook for typeahead autocomplete."""
from typing import List, Optional, Callable


class Typeahead:
    """Manages typeahead/autocomplete suggestions."""

    def __init__(self):
        self._suggestions: List[str] = []
        self._selected_index = 0
        self._filter_fn: Optional[Callable[[str], List[str]]] = None

    def set_filter(self, filter_fn: Callable[[str], List[str]]) -> None:
        """Set the filter function for suggestions."""
        self._filter_fn = filter_fn

    def update(self, query: str) -> List[str]:
        """Update suggestions based on query."""
        if self._filter_fn:
            self._suggestions = self._filter_fn(query)
        self._selected_index = 0
        return self._suggestions

    def select_next(self) -> Optional[str]:
        """Select next suggestion."""
        if self._suggestions:
            self._selected_index = (self._selected_index + 1) % len(self._suggestions)
        return self.get_selected()

    def select_previous(self) -> Optional[str]:
        """Select previous suggestion."""
        if self._suggestions:
            self._selected_index = (self._selected_index - 1) % len(self._suggestions)
        return self.get_selected()

    def get_selected(self) -> Optional[str]:
        """Get currently selected suggestion."""
        if 0 <= self._selected_index < len(self._suggestions):
            return self._suggestions[self._selected_index]
        return None

    def get_suggestions(self) -> List[str]:
        """Get all current suggestions."""
        return self._suggestions.copy()


__all__ = ['Typeahead']