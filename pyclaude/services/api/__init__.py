"""
API service for calling Anthropic.
"""

import os
from typing import Any, Optional


# Default model
DEFAULT_MODEL = 'claude-sonnet-4-20250514'


async def call_anthropic_api(
    messages: list[dict],
    tools: list[Any] | None = None,
    thinking_config: Optional[dict] = None,
    json_schema: Optional[dict] = None,
    model: Optional[str] = None,
    max_tokens: int = 8192,
    temperature: float = 1.0,
    system_prompt: Optional[str] = None,
) -> dict:
    """
    Call the Anthropic API.

    Args:
        messages: Conversation messages
        tools: Available tools
        thinking_config: Thinking configuration
        json_schema: JSON schema for output
        model: Model to use
        max_tokens: Max tokens to generate
        temperature: Temperature
        system_prompt: System prompt

    Returns:
        API response as dict
    """
    import httpx

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY not set')

    model = model or DEFAULT_MODEL

    # Build request payload
    payload: dict[str, Any] = {
        'model': model,
        'messages': messages,
        'max_tokens': max_tokens,
        'temperature': temperature,
    }

    # Add system prompt if provided
    if system_prompt:
        payload['system'] = system_prompt

    # Add tools if provided
    if tools:
        payload['tools'] = [
            {
                'name': tool.name,
                'description': tool.description,
                'input_schema': tool.input_schema if hasattr(tool, 'input_schema') else {},
            }
            for tool in tools
        ]

    # Add thinking config
    if thinking_config and thinking_config.get('type') != 'disabled':
        payload['thinking'] = thinking_config

    # Add json_schema
    if json_schema:
        payload['json_schema'] = json_schema

    # Make request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            },
            json=payload,
            timeout=300.0,
        )

        if response.status_code != 200:
            raise Exception(f'API error: {response.status_code} - {response.text}')

        data = response.json()

        # Convert to internal message format
        return _convert_response_to_message(data)


def _convert_response_to_message(data: dict) -> dict:
    """Convert API response to internal message format."""
    message = data.get('content', [])

    # Handle thinking blocks
    thinking_content = []
    text_content = []

    for block in message:
        if block.get('type') == 'thinking':
            thinking_content.append({
                'type': 'thinking',
                'thinking': block.get('thinking', ''),
            })
        elif block.get('type') == 'text':
            text_content.append({
                'type': 'text',
                'text': block.get('text', ''),
            })

    # Combine content
    combined_content = thinking_content + text_content

    return {
        'type': 'message',
        'role': 'assistant',
        'content': combined_content,
        'model': data.get('model'),
        'usage': data.get('usage', {}),
        'stop_reason': data.get('stop_reason'),
    }


async def accumulate_usage(usage: dict) -> dict:
    """Accumulate usage statistics."""
    # Placeholder - tracks cumulative API usage
    return usage


def update_usage(usage: dict, delta: dict) -> dict:
    """Update usage with delta."""
    result = dict(usage)
    for key, value in delta.items():
        result[key] = result.get(key, 0) + value
    return result


# Empty usage constant
EMPTY_USAGE = {
    'input_tokens': 0,
    'output_tokens': 0,
    'cache_creation_input_tokens': 0,
    'cache_read_input_tokens': 0,
}


__all__ = [
    'call_anthropic_api',
    'accumulate_usage',
    'update_usage',
    'EMPTY_USAGE',
    'DEFAULT_MODEL',
]