"""
Teammate mailbox utilities.

Teammate message handling.
"""

from typing import List, Dict, Any


_teammate_mailboxes: Dict[str, List[Dict[str, Any]]] = {}


def send_to_teammate(teammate_id: str, message: Dict[str, Any]) -> None:
    """Send message to teammate."""
    if teammate_id not in _teammate_mailboxes:
        _teammate_mailboxes[teammate_id] = []
    _teammate_mailboxes[teammate_id].append(message)


def get_teammate_messages(teammate_id: str) -> List[Dict[str, Any]]:
    """Get teammate messages."""
    return _teammate_mailboxes.get(teammate_id, [])


__all__ = [
    "send_to_teammate",
    "get_teammate_messages",
]