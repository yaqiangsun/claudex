"""Branded types for session and agent IDs."""
import re
from typing import NewType

# SessionId - uniquely identifies a Claude Code session
SessionId = NewType('SessionId', str)

# AgentId - uniquely identifies a subagent within a session
AgentId = NewType('AgentId', str)


def as_session_id(id: str) -> SessionId:
    """Cast a raw string to SessionId."""
    return SessionId(id)


def as_agent_id(id: str) -> AgentId:
    """Cast a raw string to AgentId."""
    return AgentId(id)


AGENT_ID_PATTERN = re.compile(r'^a(?:.+-)?[0-9a-f]{16}$')


def to_agent_id(s: str) -> AgentId | None:
    """Validate and brand a string as AgentId."""
    if AGENT_ID_PATTERN.match(s):
        return AgentId(s)
    return None


__all__ = [
    'SessionId',
    'AgentId',
    'as_session_id',
    'as_agent_id',
    'to_agent_id',
]