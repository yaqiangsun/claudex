"""Hook for LSP plugin recommendations."""


class LspPluginRecommendation:
    """Manages LSP plugin recommendations."""

    def __init__(self):
        self._recommendations = []

    def add_recommendation(self, plugin_name: str, reason: str) -> None:
        """Add a plugin recommendation."""
        self._recommendations.append({
            'plugin': plugin_name,
            'reason': reason,
        })

    def dismiss(self, plugin_name: str) -> None:
        """Dismiss a recommendation."""
        self._recommendations = [
            r for r in self._recommendations if r.get('plugin') != plugin_name
        ]

    def get_recommendations(self) -> list:
        """Get all recommendations."""
        return self._recommendations.copy()


__all__ = ['LspPluginRecommendation']