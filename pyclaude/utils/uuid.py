"""
UUID utilities.

Python adaptation.
"""

import re
import secrets
from typing import Optional

# For AgentId - we'll import from py_types later
try:
    from ..py_types import AgentId
except ImportError:
    AgentId = str  # type: ignore


UUID_REGEX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def validate_uuid(maybe_uuid: str) -> Optional[str]:
    """Validate uuid.

    Args:
        maybe_uuid: The value to check if it is a uuid

    Returns:
        UUID string or None if invalid
    """
    if not isinstance(maybe_uuid, str):
        return None

    return maybe_uuid if UUID_REGEX.match(maybe_uuid) else None


def create_agent_id(label: Optional[str] = None) -> str:
    """Generate a new agent ID with prefix.

    Format: a{label-}{16 hex chars}
    Example: aa3f2c1b4d5e6f7a8, acompact-a3f2c1b4d5e6f7a8

    Args:
        label: Optional label prefix

    Returns:
        Agent ID string
    """
    suffix = secrets.token_hex(8)
    if label:
        return f"a{label}-{suffix}"
    return f"a{suffix}"


__all__ = ["validate_uuid", "create_agent_id"]