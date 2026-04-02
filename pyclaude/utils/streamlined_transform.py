"""
Streamlined transform utilities.

Streamlined transformations.
"""

from typing import Any, Callable


def transform_streamlined(
    value: Any,
    transformers: list[Callable],
) -> Any:
    """Apply transformers in sequence."""
    result = value
    for transformer in transformers:
        result = transformer(result)
    return result


__all__ = ["transform_streamlined"]