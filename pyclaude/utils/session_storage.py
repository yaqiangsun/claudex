"""
Session storage utility.
"""
from typing import Any, Optional

_storage: dict = {}

def set_session_data(key: str, value: Any) -> None:
    _storage[key] = value

def get_session_data(key: str) -> Optional[Any]:
    return _storage.get(key)

def clear_session() -> None:
    _storage.clear()

__all__ = ['set_session_data', 'get_session_data', 'clear_session']