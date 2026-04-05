"""Base hook for plugin recommendations."""


class PluginRecommendationBase:
    """Base class for plugin recommendations."""

    def __init__(self):
        self._plugins = []
        self._dismissed = set()

    def add(self, plugin_id: str, name: str, description: str) -> None:
        """Add a plugin recommendation."""
        self._plugins.append({
            'id': plugin_id,
            'name': name,
            'description': description,
        })

    def dismiss(self, plugin_id: str) -> None:
        """Dismiss a plugin recommendation."""
        self._dismissed.add(plugin_id)

    def is_dismissed(self, plugin_id: str) -> bool:
        """Check if plugin is dismissed."""
        return plugin_id in self._dismissed

    def get_active(self) -> list:
        """Get active (non-dismissed) recommendations."""
        return [p for p in self._plugins if p['id'] not in self._dismissed]


__all__ = ['PluginRecommendationBase']