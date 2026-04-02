"""Create Direct Connect Session."""
from typing import Any


def create_direct_connect_session(
    session_id: str,
    org_uuid: str,
    config: dict[str, Any],
) -> dict:
    """Create a direct connect session."""
    return {
        'session_id': session_id,
        'org_uuid': org_uuid,
        'config': config,
    }


__all__ = ['create_direct_connect_session']