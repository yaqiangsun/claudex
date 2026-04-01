"""
Peer address parsing.

Kept separate from peer_registry.py so that SendMessageTool can import
parse_address without transitively loading the bridge modules.
"""

from typing import Dict


def parse_address(to: str) -> Dict[str, str]:
    """Parse a URI-style address into scheme + target."""
    if to.startswith('uds:'):
        return {'scheme': 'uds', 'target': to[4:]}
    if to.startswith('bridge:'):
        return {'scheme': 'bridge', 'target': to[7:]}
    # Legacy: old-code UDS senders emit bare socket paths
    if to.startswith('/'):
        return {'scheme': 'uds', 'target': to}
    return {'scheme': 'other', 'target': to}


__all__ = ["parse_address"]