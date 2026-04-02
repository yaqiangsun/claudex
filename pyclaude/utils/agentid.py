"""
Agent ID utility.

Agent ID generation and parsing.
"""

import uuid
from typing import Optional


def generate_agent_id() -> str:
    """Generate a new agent ID."""
    return str(uuid.uuid4())


def parse_agent_id(agent_id: str) -> Optional[dict]:
    """Parse an agent ID."""
    try:
        # Simple UUID parsing
        uuid.UUID(agent_id)
        return {'id': agent_id, 'type': 'agent'}
    except (ValueError, AttributeError):
        return None


def is_valid_agent_id(agent_id: str) -> bool:
    """Check if an agent ID is valid."""
    return parse_agent_id(agent_id) is not None


__all__ = ['generate_agent_id', 'parse_agent_id', 'is_valid_agent_id']