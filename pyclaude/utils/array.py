"""Array utility functions."""


def intersperse(arr: list, separator: callable) -> list:
    """Insert separator between elements of array."""
    result = []
    for i, a in enumerate(arr):
        if i:
            result.append(separator(i))
        result.append(a)
    return result


def count(arr: list, pred: callable) -> int:
    """Count elements matching predicate."""
    n = 0
    for x in arr:
        if pred(x):
            n += 1
    return n


def uniq(xs: list) -> list:
    """Remove duplicates from iterable."""
    return list(dict.fromkeys(xs))