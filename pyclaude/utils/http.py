"""
HTTP utilities.

HTTP request helpers.
"""

import os
import platform
from typing import Optional, Dict, Any
import urllib.request
import urllib.parse
import json


def get_user_agent() -> str:
    """Get the User-Agent header for API requests."""
    agent_sdk_version = os.environ.get("CLAUDE_AGENT_SDK_VERSION", "")
    if agent_sdk_version:
        agent_sdk_version = f", agent-sdk/{agent_sdk_version}"

    client_app = os.environ.get("CLAUDE_AGENT_SDK_CLIENT_APP", "")
    if client_app:
        client_app = f" {client_app}"

    return f"Claude/1.0 (Claude Code/{platform.system()}/{platform.release()}{agent_sdk_version}){client_app}"


async def http_get(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Make async HTTP GET request.

    Args:
        url: URL to fetch
        headers: Optional headers

    Returns:
        Response data
    """
    return {}


async def http_post(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Make async HTTP POST request.

    Args:
        url: URL to post to
        data: Request body
        headers: Optional headers

    Returns:
        Response data
    """
    return {}


def encode_url_params(params: Dict[str, Any]) -> str:
    """Encode URL parameters.

    Args:
        params: Parameter dict

    Returns:
        Encoded query string
    """
    return urllib.parse.urlencode(params)


__all__ = [
    "get_user_agent",
    "http_get",
    "http_post",
    "encode_url_params",
]