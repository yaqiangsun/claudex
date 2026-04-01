"""
React hook for classifierApprovals store.

Split from classifierApprovals.py so pure-state importers (permissions.py,
toolExecution.py, postCompactCleanup.py) do not pull React into print.py.
"""

from typing import Callable, Dict, Set


# Store for classifier checking status
_classifier_checking: Dict[str, bool] = {}
_subscribers: Dict[str, Set[Callable]] = {}


def is_classifier_checking(tool_use_id: str) -> bool:
    """Check if classifier is currently checking a tool use."""
    return _classifier_checking.get(tool_use_id, False)


def set_classifier_checking(tool_use_id: str, checking: bool) -> None:
    """Set classifier checking status."""
    _classifier_checking[tool_use_id] = checking
    # Notify subscribers
    if tool_use_id in _subscribers:
        for callback in _subscribers[tool_use_id]:
            callback(checking)


def subscribe_classifier_checking(tool_use_id: str, callback: Callable) -> Callable:
    """Subscribe to classifier checking changes.

    Returns unsubscribe function.
    """
    if tool_use_id not in _subscribers:
        _subscribers[tool_use_id] = set()
    _subscribers[tool_use_id].add(callback)

    def unsubscribe():
        _subscribers[tool_use_id].discard(callback)

    return unsubscribe


def use_is_classifier_checking(tool_use_id: str) -> bool:
    """Hook to check if classifier is checking a tool use."""
    return is_classifier_checking(tool_use_id)


__all__ = [
    "is_classifier_checking",
    "set_classifier_checking",
    "subscribe_classifier_checking",
    "use_is_classifier_checking",
]