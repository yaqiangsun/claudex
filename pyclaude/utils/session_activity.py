"""
Session activity utility.
"""
from typing import Dict, Any, List
from datetime import datetime

class SessionActivity:
    def __init__(self):
        self._activities: List[Dict[str, Any]] = []

    def record(self, activity_type: str, data: Any = None) -> None:
        self._activities.append({
            'type': activity_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })

    def get_activities(self) -> List[Dict[str, Any]]:
        return self._activities

_activity = SessionActivity()

def get_session_activity() -> SessionActivity:
    return _activity

__all__ = ['SessionActivity', 'get_session_activity']