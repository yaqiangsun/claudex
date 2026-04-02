"""
Filesystem operations utility.
"""
import os
from typing import Optional, Dict, Any

class FSOperations:
    def __init__(self):
        self._impl = os

    def exists(self, path: str) -> bool:
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)

    def is_dir(self, path: str) -> bool:
        return os.path.isdir(path)

    def read_file(self, path: str) -> Optional[str]:
        try:
            with open(path) as f:
                return f.read()
        except Exception:
            return None

_fs = FSOperations()

def get_fs_implementation() -> FSOperations:
    return _fs

__all__ = ['FSOperations', 'get_fs_implementation']