"""
API utility.

API client utilities.
"""

from typing import Optional, Dict, Any


class ApiClient:
    """API client."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self._headers: Dict[str, str] = {}

    def set_header(self, key: str, value: str) -> None:
        """Set a header."""
        self._headers[key] = value

    async def get(self, path: str, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        # Placeholder
        return {}

    async def post(self, path: str, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        # Placeholder
        return {}


def create_api_client(base_url: str, api_key: Optional[str] = None) -> ApiClient:
    """Create an API client."""
    return ApiClient(base_url, api_key)


__all__ = ['ApiClient', 'create_api_client']