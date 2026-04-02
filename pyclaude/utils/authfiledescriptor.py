"""
Auth file descriptor utility.

File descriptor based authentication.
"""

import os
from typing import Optional


def get_auth_file_descriptor() -> Optional[int]:
    """Get authentication file descriptor."""
    fd_str = os.environ.get('CLAUDE_CODE_AUTH_FD')
    if fd_str:
        try:
            return int(fd_str)
        except ValueError:
            pass
    return None


def is_auth_fd_valid() -> bool:
    """Check if auth file descriptor is valid."""
    fd = get_auth_file_descriptor()
    if fd is None:
        return False
    try:
        return os.fstat(fd) is not None
    except OSError:
        return False


__all__ = ['get_auth_file_descriptor', 'is_auth_fd_valid']