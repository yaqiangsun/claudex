"""
Branded types for session and agent IDs.

These prevent accidentally mixing up session IDs and agent IDs at runtime.
"""

import re
from typing import NewType, Optional


# Branded types using NewType
SessionId = NewType('SessionId', str)
AgentId = NewType('AgentId', str)


def as_session_id(id: str) -> SessionId:
    """Cast a raw string to SessionId."""
    return SessionId(id)


def as_agent_id(id: str) -> AgentId:
    """Cast a raw string to AgentId."""
    return AgentId(id)


# Agent ID pattern: a + optional label- + 16 hex chars
AGENT_ID_PATTERN = re.compile(r'^a(?:.+-)?[0-9a-f]{16}$')


def to_agent_id(s: str) -> Optional[AgentId]:
    """Validate and brand a string as AgentId.

    Returns None if the string doesn't match.
    """
    if AGENT_ID_PATTERN.match(s):
        return AgentId(s)
    return None


__all__ = [
    "SessionId",
    "AgentId",
    "as_session_id",
    "as_agent_id",
    "to_agent_id",
]