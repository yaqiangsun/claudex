"""
Session storage portable utility.
"""
from typing import Any, Optional
import os
import json

def get_portable_storage_path() -> Optional[str]:
    return os.environ.get('CLAUDE_CODE_STORAGE_PATH')

def set_portable_data(key: str, value: Any) -> bool:
    return False

def get_portable_data(key: str) -> Optional[Any]:
    return None

__all__ = ['get_portable_storage_path', 'set_portable_data', 'get_portable_data']