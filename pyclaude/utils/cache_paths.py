"""
Cache path utilities.

Python adaptation.
"""

import os
import hashlib
from pathlib import Path
from typing import Optional

# Try to get cache directory
def _get_cache_base() -> str:
    """Get base cache directory."""
    # Use XDG_CACHE_HOME or ~/.cache
    cache_home = os.environ.get("XDG_CACHE_HOME")
    if cache_home:
        return os.path.join(cache_home, "claude-cli")

    home = os.path.expanduser("~")
    return os.path.join(home, ".cache", "claude-cli")


# Max length for sanitized path names
_MAX_SANITIZED_LENGTH = 200


def _djb2_hash(s: str) -> int:
    """Simple hash function."""
    h = 5381
    for c in s:
        h = ((h << 5) + h) + ord(c)
    return h & 0xFFFFFFFF


def _sanitize_path(name: str) -> str:
    """Sanitize a path name for filesystem compatibility."""
    sanitized = "".join(c if c.isalnum() else "-" for c in name)
    if len(sanitized) <= _MAX_SANITIZED_LENGTH:
        return sanitized
    hash_suffix = str(abs(_djb2_hash(name)))
    return f"{sanitized[:_MAX_SANITIZED_LENGTH]}-{hash_suffix}"


def _get_project_dir(cwd: str) -> str:
    """Get project-specific directory name."""
    return _sanitize_path(cwd)


class CachePaths:
    """Cache path management."""

    def __init__(self, cwd: Optional[str] = None):
        self._cwd = cwd or os.getcwd()
        self._base = _get_cache_base()

    def base_logs(self) -> str:
        """Base logs directory."""
        return os.path.join(self._base, _get_project_dir(self._cwd))

    def errors(self) -> str:
        """Errors directory."""
        return os.path.join(self.base_logs(), "errors")

    def messages(self) -> str:
        """Messages directory."""
        return os.path.join(self.base_logs(), "messages")

    def mcp_logs(self, server_name: str) -> str:
        """MCP logs directory for a specific server."""
        sanitized_name = _sanitize_path(server_name)
        return os.path.join(self.base_logs(), f"mcp-logs-{sanitized_name}")


# Global instance
_cache_paths: Optional[CachePaths] = None


def get_cache_paths(cwd: Optional[str] = None) -> CachePaths:
    """Get cache paths instance."""
    global _cache_paths
    if _cache_paths is None:
        _cache_paths = CachePaths(cwd)
    return _cache_paths


__all__ = ["CachePaths", "get_cache_paths"]