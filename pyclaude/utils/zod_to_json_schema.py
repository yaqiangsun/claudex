"""
Zod to JSON schema utilities.

Convert Zod schemas to JSON schema.
"""

from typing import Any, Dict


def zod_to_json_schema(zod_schema: Any) -> Dict[str, Any]:
    """Convert Zod schema to JSON schema."""
    # Placeholder - would parse Zod schema
    return {"type": "object"}


__all__ = ["zod_to_json_schema"]