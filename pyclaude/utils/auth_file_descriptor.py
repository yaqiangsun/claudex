"""
Auth file descriptor utilities.

File descriptor based authentication.
"""

import os
from typing import Optional


def get_auth_file_descriptor() -> Optional[int]:
    """Get authentication file descriptor.

    Returns:
        File descriptor or None
    """
    fd_str = os.environ.get("CLAUDE_CODE_AUTH_FD")
    if fd_str:
        try:
            return int(fd_str)
        except ValueError:
            pass
    return None


def read_from_auth_fd() -> Optional[bytes]:
    """Read from auth file descriptor.

    Returns:
        Data or None
    """
    fd = get_auth_file_descriptor()
    if fd is not None:
        try:
            return os.read(fd, 4096)
        except Exception:
            pass
    return None


__all__ = [
    "get_auth_file_descriptor",
    "read_from_auth_fd",
]