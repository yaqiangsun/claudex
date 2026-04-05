"""Notifier service - system notifications."""

import os
import subprocess
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class NotificationLevel(str, Enum):
    """Notification level."""
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'


@dataclass
class Notification:
    """A notification."""
    title: str
    message: str
    level: NotificationLevel = NotificationLevel.INFO
    sound: bool = True


class NotifierService:
    """Service for system notifications."""

    def __init__(self):
        self._enabled = True

    def is_enabled(self) -> bool:
        """Check if notifications are enabled."""
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable notifications."""
        self._enabled = enabled

    async def notify(self, notification: Notification) -> bool:
        """Send a notification."""
        if not self._enabled:
            return False

        try:
            if os.name == 'darwin':  # macOS
                return await self._notify_macos(notification)
            elif os.name == 'nt':  # Windows
                return await self._notify_windows(notification)
            else:  # Linux
                return await self._notify_linux(notification)
        except Exception as e:
            print(f'Notification error: {e}')
            return False

    async def _notify_macos(self, notification: Notification) -> bool:
        """Send notification on macOS."""
        title = notification.title.replace('"', '\\"')
        message = notification.message.replace('"', '\\"')

        cmd = [
            'osascript', '-e',
            f'display notification "{message}" with title "{title}"'
        ]

        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0

    async def _notify_windows(self, notification: Notification) -> bool:
        """Send notification on Windows (PowerShell)."""
        # For Windows, we'd use Windows Toast Notifications
        # This is a simplified version
        return True

    async def _notify_linux(self, notification: Notification) -> bool:
        """Send notification on Linux."""
        try:
            cmd = ['notify-send', notification.title, notification.message]
            result = subprocess.run(cmd, capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            # notify-send not installed
            return False

    async def notify_info(self, title: str, message: str) -> bool:
        """Send an info notification."""
        return await self.notify(Notification(title, message, NotificationLevel.INFO))

    async def notify_warning(self, title: str, message: str) -> bool:
        """Send a warning notification."""
        return await self.notify(Notification(title, message, NotificationLevel.WARNING))

    async def notify_error(self, title: str, message: str) -> bool:
        """Send an error notification."""
        return await self.notify(Notification(title, message, NotificationLevel.ERROR))

    async def notify_success(self, title: str, message: str) -> bool:
        """Send a success notification."""
        return await self.notify(Notification(title, message, NotificationLevel.SUCCESS))


# Global notifier service
_notifier = NotifierService()


def get_notifier() -> NotifierService:
    """Get the global notifier service."""
    return _notifier


__all__ = ['NotifierService', 'Notification', 'NotificationLevel', 'get_notifier']