"""
AWS auth status manager utilities.

Track AWS authentication status.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AwsAuthStatus:
    """AWS authentication status."""
    authenticated: bool
    profile: Optional[str] = None
    region: Optional[str] = None
    expires_at: Optional[datetime] = None


class AwsAuthStatusManager:
    """Manage AWS auth status."""

    def __init__(self):
        self._status: Optional[AwsAuthStatus] = None

    def set_status(self, status: AwsAuthStatus) -> None:
        """Set auth status."""
        self._status = status

    def get_status(self) -> Optional[AwsAuthStatus]:
        """Get auth status."""
        return self._status

    def is_authenticated(self) -> bool:
        """Check if authenticated."""
        return self._status is not None and self._status.authenticated


_manager = AwsAuthStatusManager()


def get_aws_auth_manager() -> AwsAuthStatusManager:
    """Get global AWS auth manager."""
    return _manager


__all__ = [
    "AwsAuthStatus",
    "AwsAuthStatusManager",
    "get_aws_auth_manager",
]