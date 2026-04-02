"""
Set utilities - optimized set operations.

Python adaptation.
"""

from typing import TypeVar, Set, FrozenSet, Iterator

A = TypeVar("A")


def difference(a: Set[A], b: Set[A]) -> Set[A]:
    """Return items in a that are not in b."""
    result: Set[A] = set()
    for item in a:
        if item not in b:
            result.add(item)
    return result


def intersects(a: Set[A], b: Set[A]) -> bool:
    """Check if sets have any common elements."""
    if len(a) == 0 or len(b) == 0:
        return False
    for item in a:
        if item in b:
            return True
    return False


def every(a: FrozenSet[A], b: FrozenSet[A]) -> bool:
    """Check if all items in a are in b."""
    for item in a:
        if item not in b:
            return False
    return True


def union(a: Set[A], b: Set[A]) -> Set[A]:
    """Return union of two sets."""
    result: Set[A] = set(a)
    result.update(b)
    return result


__all__ = ["difference", "intersects", "every", "union"]