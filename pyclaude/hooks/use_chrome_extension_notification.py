"""Hook for Chrome extension notifications."""


class ChromeExtensionNotification:
    """Manages Chrome extension integration notifications."""

    def __init__(self):
        self._notifications = []

    def show(self, message: str, notification_type: str = "info") -> None:
        """Show a notification."""
        self._notifications.append({
            'message': message,
            'type': notification_type,
        })

    def dismiss(self, notification_id: str) -> None:
        """Dismiss a notification."""
        self._notifications = [n for n in self._notifications if n.get('id') != notification_id]

    def get_notifications(self) -> list:
        """Get all active notifications."""
        return self._notifications.copy()


__all__ = ['ChromeExtensionNotification']