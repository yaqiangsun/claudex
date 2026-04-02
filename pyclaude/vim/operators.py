"""Vim Operator Functions."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import Operator, FindType, TextObjScope, RecordedChange, OperatorContext


def execute_operator_motion(
    op: 'Operator',
    motion: str,
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute an operator with a simple motion."""
    from .motions import resolve_motion

    target = resolve_motion(motion, ctx['cursor'], count)
    if target == ctx['cursor']:
        return

    # Simplified implementation
    ctx.get('record_change', lambda x: None)({
        'type': 'operator',
        'op': op,
        'motion': motion,
        'count': count,
    })


def execute_operator_find(
    op: 'Operator',
    find_type: 'FindType',
    char: str,
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute an operator with a find motion."""
    ctx.get('record_change', lambda x: None)({
        'type': 'operatorFind',
        'op': op,
        'find': find_type,
        'char': char,
        'count': count,
    })


def execute_operator_text_obj(
    op: 'Operator',
    scope: 'TextObjScope',
    obj_type: str,
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute an operator with a text object."""
    ctx.get('record_change', lambda x: None)({
        'type': 'operatorTextObj',
        'op': op,
        'obj_type': obj_type,
        'scope': scope,
        'count': count,
    })


def execute_line_op(
    op: 'Operator',
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute a line operation (dd, cc, yy)."""
    text = ctx['text']
    lines = text.split('\n')

    # Find current line
    current_line = text[: ctx['cursor'].offset].count('\n')
    lines_to_affect = min(count, len(lines) - current_line)

    # Simplified implementation
    ctx.get('record_change', lambda x: None)({
        'type': 'operator',
        'op': op,
        'motion': op[0],
        'count': count,
    })


def execute_x(count: int, ctx: 'OperatorContext') -> None:
    """Execute delete character (x command)."""
    ctx.get('record_change', lambda x: None)({'type': 'x', 'count': count})


def execute_replace(
    char: str,
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute replace character (r command)."""
    ctx.get('record_change', lambda x: None)({
        'type': 'replace',
        'char': char,
        'count': count,
    })


def execute_toggle_case(count: int, ctx: 'OperatorContext') -> None:
    """Execute toggle case (~ command)."""
    ctx.get('record_change', lambda x: None)({
        'type': 'toggleCase',
        'count': count,
    })


def execute_join(count: int, ctx: 'OperatorContext') -> None:
    """Execute join lines (J command)."""
    ctx.get('record_change', lambda x: None)({'type': 'join', 'count': count})


def execute_paste(
    after: bool,
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute paste (p/P command)."""
    pass  # Implementation depends on register state


def execute_indent(
    dir: str,
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute indent (>> command)."""
    ctx.get('record_change', lambda x: None)({
        'type': 'indent',
        'dir': dir,
        'count': count,
    })


def execute_open_line(
    direction: str,
    ctx: 'OperatorContext',
) -> None:
    """Execute open line (o/O command)."""
    ctx.get('record_change', lambda x: None)({
        'type': 'openLine',
        'direction': direction,
    })


def execute_operator_g(
    op: 'Operator',
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute operator with G motion."""
    ctx.get('record_change', lambda x: None)({
        'type': 'operator',
        'op': op,
        'motion': 'G',
        'count': count,
    })


def execute_operator_gg(
    op: 'Operator',
    count: int,
    ctx: 'OperatorContext',
) -> None:
    """Execute operator with gg motion."""
    ctx.get('record_change', lambda x: None)({
        'type': 'operator',
        'op': op,
        'motion': 'gg',
        'count': count,
    })


__all__ = [
    'execute_operator_motion',
    'execute_operator_find',
    'execute_operator_text_obj',
    'execute_line_op',
    'execute_x',
    'execute_replace',
    'execute_toggle_case',
    'execute_join',
    'execute_paste',
    'execute_indent',
    'execute_open_line',
    'execute_operator_g',
    'execute_operator_gg',
]