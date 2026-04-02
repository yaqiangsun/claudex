"""Vim Motion Functions."""
from .types import FindType


def resolve_motion(key: str, cursor, count: int):
    """Resolve a motion to a target cursor position."""
    result = cursor
    for _ in range(count):
        next_pos = _apply_single_motion(key, result)
        if next_pos == result:
            break
        result = next_pos
    return result


def _apply_single_motion(key: str, cursor):
    """Apply a single motion step."""
    motion_map = {
        'h': lambda c: c.left(),
        'l': lambda c: c.right(),
        'j': lambda c: c.down_logical_line(),
        'k': lambda c: c.up_logical_line(),
        'gj': lambda c: c.down(),
        'gk': lambda c: c.up(),
        'w': lambda c: c.next_vim_word(),
        'b': lambda c: c.prev_vim_word(),
        'e': lambda c: c.end_of_vim_word(),
        'W': lambda c: c.next_word(),
        'B': lambda c: c.prev_word(),
        'E': lambda c: c.end_of_word(),
        '0': lambda c: c.start_of_logical_line(),
        '^': lambda c: c.first_non_blank_in_logical_line(),
        '$': lambda c: c.end_of_logical_line(),
        'G': lambda c: c.start_of_last_line(),
    }

    motion_func = motion_map.get(key)
    if motion_func:
        return motion_func(cursor)
    return cursor


def is_inclusive_motion(key: str) -> bool:
    """Check if a motion is inclusive."""
    return key in 'eE$'


def is_linewise_motion(key: str) -> bool:
    """Check if a motion is linewise."""
    return key in 'jkG' or key == 'gg'


__all__ = [
    'resolve_motion',
    'is_inclusive_motion',
    'is_linewise_motion',
]