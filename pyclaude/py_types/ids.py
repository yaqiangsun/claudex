"""
Branded types for session and agent IDs.
These prevent accidentally mixing up session IDs and agent IDs at runtime.
"""

from typing import NewType, Optional, Pattern

# SessionId: uniquely identifies a Claude Code session
SessionId = NewType('SessionId', str)

# AgentId: uniquely identifies a subagent within a session
AgentId = NewType('AgentId', str)


def as_session_id(id: str) -> SessionId:
    """Cast a raw string to SessionId."""
    return SessionId(id)


def as_agent_id(id: str) -> AgentId:
    """Cast a raw string to AgentId."""
    return AgentId(id)


AGENT_ID_PATTERN: Pattern = r'^a(?:.+-)?[0-9a-f]{16}$'


def to_agent_id(s: str) -> Optional[AgentId]:
    """
    Validate and brand a string as AgentId.
    Matches the format: `a` + optional `<label>-` + 16 hex chars.
    Returns None if the string doesn't match.
    """
    import re
    if re.match(AGENT_ID_PATTERN, s):
        return AgentId(s)
    return None