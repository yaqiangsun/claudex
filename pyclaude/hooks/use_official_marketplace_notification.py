"""Hook for official marketplace notifications."""


class OfficialMarketplaceNotification:
    """Manages official marketplace notifications."""

    def __init__(self):
        self._notifications = []

    def show(self, title: str, message: str, action_url: Optional[str] = None) -> None:
        """Show a marketplace notification."""
        self._notifications.append({
            'title': title,
            'message': message,
            'action_url': action_url,
        })

    def dismiss(self, index: int) -> None:
        """Dismiss a notification by index."""
        if 0 <= index < len(self._notifications):
            self._notifications.pop(index)

    def get_notifications(self) -> list:
        """Get all notifications."""
        return self._notifications.copy()


from typing import Optional
__all__ = ['OfficialMarketplaceNotification']