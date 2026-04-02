"""
Query context utilities.

Context for query operations.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class QueryContext:
    """Context for query operations."""
    query: str
    model: str
    max_tokens: Optional[int] = None
    temperature: float = 1.0
    system_prompt: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, str]] = field(default_factory=list)


def create_query_context(
    query: str,
    model: str,
    **kwargs,
) -> QueryContext:
    """Create query context.

    Args:
        query: User query
        model: Model to use
        **kwargs: Additional context options

    Returns:
        Query context
    """
    return QueryContext(
        query=query,
        model=model,
        **kwargs,
    )


def add_to_history(
    context: QueryContext,
    role: str,
    content: str,
) -> None:
    """Add message to query history.

    Args:
        context: Query context
        role: Message role
        content: Message content
    """
    context.history.append({
        "role": role,
        "content": content,
    })


async def fetch_system_prompt_parts(
    tools: list,
    main_loop_model: str,
    additional_working_directories: list = None,
    mcp_clients: list = None,
    custom_system_prompt: str = None,
    append_system_prompt: str = None,
) -> dict:
    """Fetch system prompt parts for the API."""
    # Simplified implementation
    from ..context import get_system_prompt, get_user_context, get_system_context

    if custom_system_prompt is not None:
        default_system_prompt = []
        system_context = {}
    else:
        default_system_prompt = await get_system_prompt(
            tools,
            main_loop_model,
            additional_working_directories or [],
            mcp_clients or [],
        )
        system_context = await get_system_context()

    user_context = await get_user_context()

    return {
        'default_system_prompt': default_system_prompt,
        'user_context': user_context,
        'system_context': system_context,
    }


__all__ = [
    "QueryContext",
    "create_query_context",
    "add_to_history",
    "fetch_system_prompt_parts",
]