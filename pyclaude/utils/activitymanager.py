"""
Activity manager utility.

Manages activity tracking.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Activity:
    """Represents an activity."""
    id: str
    type: str
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)


class ActivityManager:
    """Manages activity tracking."""

    def __init__(self):
        self._activities: List[Activity] = []
        self._max_size = 1000

    def record(self, activity_type: str, data: Optional[Dict[str, Any]] = None) -> Activity:
        """Record an activity."""
        import uuid
        activity = Activity(
            id=str(uuid.uuid4()),
            type=activity_type,
            data=data or {},
        )
        self._activities.append(activity)
        if len(self._activities) > self._max_size:
            self._activities.pop(0)
        return activity

    def get_recent(self, count: int = 10) -> List[Activity]:
        """Get recent activities."""
        return self._activities[-count:]

    def clear(self) -> None:
        """Clear all activities."""
        self._activities = []


# Global instance
_activity_manager = ActivityManager()


def get_activity_manager() -> ActivityManager:
    """Get the global activity manager."""
    return _activity_manager


__all__ = ['Activity', 'ActivityManager', 'get_activity_manager']