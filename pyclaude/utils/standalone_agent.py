"""
Standalone agent utilities.

Standalone agent handling.
"""

from typing import Optional, Dict, Any


def create_standalone_agent(name: str, config: Dict[str, Any]) -> str:
    """Create a standalone agent."""
    import uuid
    return str(uuid.uuid4())


def get_standalone_agent(agent_id: str) -> Optional[Dict[str, Any]]:
    """Get standalone agent."""
    return None


__all__ = [
    "create_standalone_agent",
    "get_standalone_agent",
]