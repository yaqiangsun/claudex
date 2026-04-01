"""Crypto utilities - wraps Python's secrets module."""

import uuid


def random_uuid() -> str:
    """Generate a random UUID."""
    return str(uuid.uuid4())