"""
mTLS utilities.

Mutual TLS handling.
"""

import os
from typing import Optional, Dict, Any


def get_mtls_config() -> Dict[str, Any]:
    """Get mTLS configuration."""
    return {
        "client_cert": os.environ.get("CLAUDE_CODE_CLIENT_CERT"),
        "client_key": os.environ.get("CLAUDE_CODE_CLIENT_KEY"),
        "ca_cert": os.environ.get("CLAUDE_CODE_CA_CERT"),
    }


def is_mtls_enabled() -> bool:
    """Check if mTLS is enabled."""
    config = get_mtls_config()
    return bool(config["client_cert"] and config["client_key"])


__all__ = [
    "get_mtls_config",
    "is_mtls_enabled",
]