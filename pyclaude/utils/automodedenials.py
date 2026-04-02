"""
Auto mode denials utility.

Track auto mode denial reasons.
"""

from typing import List, Dict, Any
from datetime import datetime


class AutoModeDenials:
    """Track auto mode denial reasons."""

    def __init__(self):
        self._denials: List[Dict[str, Any]] = []

    def record_denial(self, reason: str, details: Any = None) -> None:
        """Record a denial."""
        self._denials.append({
            'reason': reason,
            'details': details,
            'timestamp': datetime.now().isoformat(),
        })

    def get_denials(self) -> List[Dict[str, Any]]:
        """Get all denials."""
        return self._denials.copy()

    def clear(self) -> None:
        """Clear denials."""
        self._denials = []

    def has_denials(self) -> bool:
        """Check if there are any denials."""
        return len(self._denials) > 0


# Global instance
_denials = AutoModeDenials()


def get_auto_mode_denials() -> AutoModeDenials:
    """Get global auto mode denials tracker."""
    return _denials


__all__ = ['AutoModeDenials', 'get_auto_mode_denials']