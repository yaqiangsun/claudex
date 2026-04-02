"""
MCP output storage utility.
"""
from typing import Any, Dict

_storage: Dict[str, Any] = {}

def store_mcp_output(key: str, value: Any) -> None:
    _storage[key] = value

def get_mcp_output(key: str) -> Any:
    return _storage.get(key)

__all__ = ['store_mcp_output', 'get_mcp_output']