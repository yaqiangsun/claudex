"""
Generators utilities.

Code generation helpers.
"""

from typing import Iterator, TypeVar, Callable, Any

T = TypeVar("T")


def generate_items(
    generator_fn: Callable[[], Iterator[T]],
    count: int,
) -> list:
    """Generate items from generator."""
    result = []
    for item in generator_fn():
        if len(result) >= count:
            break
        result.append(item)
    return result


def chunk_generator(generator: Iterator[T], size: int) -> Iterator[list]:
    """Chunk generator into batches."""
    chunk = []
    for item in generator:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


__all__ = [
    "generate_items",
    "chunk_generator",
]