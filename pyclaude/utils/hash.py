"""
Hash utilities.

Hashing functions.
"""

import hashlib
from typing import Optional


def hash_string(text: str, algorithm: str = "sha256") -> str:
    """Hash a string."""
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode())
    return hasher.hexdigest()


def hash_file(path: str, algorithm: str = "sha256") -> Optional[str]:
    """Hash a file."""
    try:
        hasher = hashlib.new(algorithm)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None


__all__ = [
    "hash_string",
    "hash_file",
]