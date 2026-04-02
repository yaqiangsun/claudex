"""API client for Anthropic."""
import os
import uuid
from typing import Any, Optional

import httpx


class AnthropicClient:
    """Anthropic API client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.anthropic.com",
        max_retries: int = 3,
        timeout: int = 600000,
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._session_id = str(uuid.uuid4())

    async def get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None:
            headers = await self._get_headers()
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=httpx.Timeout(self.timeout / 1000),
            )
        return self._client

    async def _get_headers(self) -> dict[str, str]:
        """Get request headers."""
        from ...utils.auth import get_anthropic_api_key, is_claude_ai_subscriber
        from ...utils.http import get_user_agent

        headers = {
            "x-app": "cli",
            "User-Agent": get_user_agent(),
            "x-claude-code-session-id": self._session_id,
            "anthropic-version": "2023-06-01",
        }

        if not is_claude_ai_subscriber():
            api_key = self.api_key or get_anthropic_api_key()
            if api_key:
                headers["x-api-key"] = api_key

        return headers

    async def create_message(
        self,
        model: str,
        messages: list[dict],
        system: Optional[str] = None,
        tools: Optional[list[dict]] = None,
        max_tokens: int = 4096,
        stream: bool = False,
        extra_headers: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        """Create a message with the Anthropic API."""
        client = await self.get_client()

        headers = await self._get_headers()
        if extra_headers:
            headers.update(extra_headers)

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        if system:
            payload["system"] = system

        if tools:
            payload["tools"] = tools

        # Add extra params from kwargs
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value

        # Select endpoint
        endpoint = "/v1/messages"
        if stream:
            endpoint = "/v1/messages"

        response = await client.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    async def create_message_stream(
        self,
        model: str,
        messages: list[dict],
        system: Optional[str] = None,
        tools: Optional[list[dict]] = None,
        max_tokens: int = 4096,
        **kwargs,
    ):
        """Create a streaming message with the Anthropic API."""
        client = await self.get_client()

        headers = await self._get_headers()
        headers["accept"] = "text/event-stream"

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": True,
        }

        if system:
            payload["system"] = system

        if tools:
            payload["tools"] = tools

        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value

        async with client.stream("POST", "/v1/messages", json=payload, headers=headers) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    yield line[6:]

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None


# Global client instance
_client: Optional[AnthropicClient] = None


async def get_anthropic_client(
    api_key: Optional[str] = None,
    max_retries: int = 3,
    model: Optional[str] = None,
) -> AnthropicClient:
    """Get or create the Anthropic client."""
    global _client
    if _client is None:
        _client = AnthropicClient(
            api_key=api_key,
            max_retries=max_retries,
        )
    return _client


async def close_anthropic_client():
    """Close the Anthropic client."""
    global _client
    if _client:
        await _client.close()
        _client = None


__all__ = [
    "AnthropicClient",
    "get_anthropic_client",
    "close_anthropic_client",
]