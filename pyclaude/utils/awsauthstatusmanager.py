"""
AWS auth status manager utility.

Manage AWS authentication status.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class AWSAuthStatusManager:
    """Manage AWS authentication status."""

    def __init__(self):
        self._status: Dict[str, Any] = {}

    def set_authenticated(self, profile: str, expires_at: Optional[datetime] = None) -> None:
        """Set authenticated status."""
        self._status[profile] = {
            'authenticated': True,
            'expires_at': expires_at,
            'last_check': datetime.now(),
        }

    def is_authenticated(self, profile: str) -> bool:
        """Check if profile is authenticated."""
        if profile not in self._status:
            return False
        status = self._status[profile]
        if not status.get('authenticated'):
            return False
        expires_at = status.get('expires_at')
        if expires_at and expires_at < datetime.now():
            return False
        return True

    def clear(self, profile: Optional[str] = None) -> None:
        """Clear authentication status."""
        if profile:
            self._status.pop(profile, None)
        else:
            self._status = {}


# Global instance
_aws_auth_manager = AWSAuthStatusManager()


def get_aws_auth_status_manager() -> AWSAuthStatusManager:
    """Get global AWS auth status manager."""
    return _aws_auth_manager


__all__ = ['AWSAuthStatusManager', 'get_aws_auth_status_manager']