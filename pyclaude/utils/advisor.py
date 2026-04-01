"""
Advisor tool types and utilities.
"""

from typing import Dict, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class AdvisorServerToolUseBlock:
    """Server tool use block for advisor."""
    type: str = 'server_tool_use'
    id: str = ''
    name: str = 'advisor'
    input: Dict[str, Any] = None

    def __post_init__(self):
        if self.input is None:
            self.input = {}


@dataclass
class AdvisorResultBlock:
    """Advisor result block."""
    type: str
    tool_use_id: str
    content: Union[Dict[str, str], Dict[str, str], Dict[str, str]]


def is_advisor_block(param: Dict[str, Any]) -> bool:
    """Check if a block is an advisor block."""
    if param.get("type") == "server_tool_use" and param.get("name") == "advisor":
        return True
    if param.get("type") == "advisor_tool_result":
        return True
    return False


def model_supports_advisor(model: str) -> bool:
    """Check if a model supports the advisor feature."""
    # Advisor requires certain model capabilities
    # Placeholder implementation
    return True


def is_valid_advisor_model(model: str) -> bool:
    """Check if a model is valid for advisor."""
    # Advisor models are typically opus, sonnet, etc.
    # Placeholder implementation
    return model in ["opus", "sonnet", "haiku", "claude-opus-4-6", "claude-sonnet-4-6"]


def can_user_configure_advisor() -> bool:
    """Check if user can configure advisor."""
    # Placeholder - would check permissions
    return True


__all__ = [
    "AdvisorServerToolUseBlock",
    "AdvisorResultBlock",
    "is_advisor_block",
    "model_supports_advisor",
    "is_valid_advisor_model",
    "can_user_configure_advisor",
]