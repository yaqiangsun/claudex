"""Hook for Claude Code hint recommendations."""


class ClaudeCodeHintRecommendation:
    """Manages hint recommendations for Claude Code features."""

    def __init__(self):
        self._hints = []
        self._dismissed = set()

    def add_hint(self, hint: str, category: str = "general") -> None:
        """Add a new hint recommendation."""
        self._hints.append({'text': hint, 'category': category})

    def dismiss_hint(self, hint_id: str) -> None:
        """Dismiss a hint so it won't be shown again."""
        self._dismissed.add(hint_id)

    def get_active_hints(self) -> list:
        """Get all active (non-dismissed) hints."""
        return [h for h in self._hints if h.get('id') not in self._dismissed]


__all__ = ['ClaudeCodeHintRecommendation']