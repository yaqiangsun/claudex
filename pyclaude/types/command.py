"""Command types."""
from typing import Any, TypedDict


class Command(TypedDict):
    """Command definition."""

    type: str
    name: str
    description: str
    has_user_specified_description: bool
    allowed_tools: list[str]
    argument_hint: str | None
    when_to_use: str | None
    model: str | None
    disable_model_invocation: bool
    user_invocable: bool
    content_length: int
    source: str
    loaded_from: str
    hooks: list | None
    context: dict | None
    agent: dict | None
    is_enabled: callable | None
    is_hidden: bool
    progress_message: str
    get_prompt_for_command: callable | None


__all__ = ['Command']