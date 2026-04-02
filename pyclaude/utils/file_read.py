"""
File read utility.
"""
from typing import Optional

def read_file(path: str, encoding: str = 'utf-8') -> Optional[str]:
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception:
        return None

__all__ = ['read_file']