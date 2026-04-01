"""
Types module - Type definitions for Claude Code.

Python adaptation of TypeScript type definitions.
"""

from .ids import SessionId, AgentId, as_session_id, as_agent_id, to_agent_id
from .command import (
    CommandSource,
    LocalCommandResult,
    PromptCommand,
    text_result,
    compact_result,
    skip_result,
)

__all__ = [
    "SessionId",
    "AgentId",
    "as_session_id",
    "as_agent_id",
    "to_agent_id",
    "CommandSource",
    "LocalCommandResult",
    "PromptCommand",
    "text_result",
    "compact_result",
    "skip_result",
]