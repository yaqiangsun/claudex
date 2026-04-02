"""
Read file in range utility.
"""
from typing import Optional

def read_file_in_range(path: str, start: int, end: int) -> Optional[str]:
    try:
        with open(path) as f:
            f.seek(start)
            return f.read(end - start)
    except Exception:
        return None

__all__ = ['read_file_in_range']