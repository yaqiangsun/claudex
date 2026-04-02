"""Vim Mode State Machine Types."""
from typing import Literal, TypedDict


class OperatorContext(TypedDict):
    """Context for operator execution."""

    cursor: object  # Cursor object
    text: str
    setText: object  # callable
    setOffset: object  # callable
    enterInsert: object  # callable
    getRegister: object  # callable
    setRegister: object  # callable
    getLastFind: object  # callable
    setLastFind: object  # callable
    recordChange: object  # callable


Operator = Literal['delete', 'change', 'yank']
FindType = Literal['f', 'F', 't', 'T']
TextObjScope = Literal['inner', 'around']


# VimState - Complete vim state
class InsertModeState:
    def __init__(self, inserted_text: str = ''):
        self.mode = 'INSERT'
        self.inserted_text = inserted_text


class NormalModeState:
    def __init__(self, command: 'CommandState'):
        self.mode = 'NORMAL'
        self.command = command


VimState = InsertModeState | NormalModeState


# CommandState - Command state machine for NORMAL mode
class IdleState:
    type: str = 'idle'


class CountState:
    type: str = 'count'
    digits: str


class OperatorState:
    type: str = 'operator'
    op: Operator
    count: int


class OperatorCountState:
    type: str = 'operatorCount'
    op: Operator
    count: int
    digits: str


class OperatorFindState:
    type: str = 'operatorFind'
    op: Operator
    count: int
    find: FindType


class OperatorTextObjState:
    type: str = 'operatorTextObj'
    op: Operator
    count: int
    scope: TextObjScope


class FindState:
    type: str = 'find'
    find: FindType
    count: int


class GState:
    type: str = 'g'
    count: int


class OperatorGState:
    type: str = 'operatorG'
    op: Operator
    count: int


class ReplaceState:
    type: str = 'replace'
    count: int


class IndentState:
    type: str = 'indent'
    dir: Literal['>', '<']
    count: int


CommandState = (
    IdleState
    | CountState
    | OperatorState
    | OperatorCountState
    | OperatorFindState
    | OperatorTextObjState
    | FindState
    | GState
    | OperatorGState
    | ReplaceState
    | IndentState
)


# PersistentState - Persistent state across commands
class PersistentState:
    def __init__(
        self,
        last_change: 'RecordedChange | None' = None,
        last_find: dict | None = None,
        register: str = '',
        register_is_linewise: bool = False,
    ):
        self.last_change = last_change
        self.last_find = last_find
        self.register = register
        self.register_is_linewise = register_is_linewise


# RecordedChange - For dot-repeat
class InsertChange:
    type: str = 'insert'
    text: str


class OperatorChange:
    type: str = 'operator'
    op: Operator
    motion: str
    count: int


class OperatorTextObjChange:
    type: str = 'operatorTextObj'
    op: Operator
    obj_type: str
    scope: TextObjScope
    count: int


class OperatorFindChange:
    type: str = 'operatorFind'
    op: Operator
    find: FindType
    char: str
    count: int


class ReplaceChange:
    type: str = 'replace'
    char: str
    count: int


class XChange:
    type: str = 'x'
    count: int


class ToggleCaseChange:
    type: str = 'toggleCase'
    count: int


class IndentChange:
    type: str = 'indent'
    dir: Literal['>', '<']
    count: int


class OpenLineChange:
    type: str = 'openLine'
    direction: Literal['above', 'below']


class JoinChange:
    type: str = 'join'
    count: int


RecordedChange = (
    InsertChange
    | OperatorChange
    | OperatorTextObjChange
    | OperatorFindChange
    | ReplaceChange
    | XChange
    | ToggleCaseChange
    | IndentChange
    | OpenLineChange
    | JoinChange
)


# Key Groups
OPERATORS = {
    'd': 'delete',
    'c': 'change',
    'y': 'yank',
}


def is_operator_key(key: str) -> bool:
    """Check if key is an operator key."""
    return key in OPERATORS


SIMPLE_MOTIONS = {
    'h',
    'l',
    'j',
    'k',  # Basic movement
    'w',
    'b',
    'e',
    'W',
    'B',
    'E',  # Word motions
    '0',
    '^',
    '$',  # Line positions
}

FIND_KEYS = {'f', 'F', 't', 'T'}

TEXT_OBJ_SCOPES = {
    'i': 'inner',
    'a': 'around',
}


def is_text_obj_scope_key(key: str) -> bool:
    """Check if key is a text object scope key."""
    return key in TEXT_OBJ_SCOPES


TEXT_OBJ_TYPES = {
    'w',
    'W',  # Word/WORD
    '"',
    "'",
    '`',  # Quotes
    '(',
    ')',
    'b',  # Parens
    '[',
    ']',  # Brackets
    '{',
    '}',
    'B',  # Braces
    '<',
    '>',  # Angle brackets
}

MAX_VIM_COUNT = 10000


def create_initial_vim_state() -> VimState:
    """Create initial vim state."""
    return InsertModeState(inserted_text='')


def create_initial_persistent_state() -> PersistentState:
    """Create initial persistent state."""
    return PersistentState(
        last_change=None,
        last_find=None,
        register='',
        register_is_linewise=False,
    )


__all__ = [
    'Operator',
    'FindType',
    'TextObjScope',
    'VimState',
    'CommandState',
    'PersistentState',
    'RecordedChange',
    'OPERATORS',
    'SIMPLE_MOTIONS',
    'FIND_KEYS',
    'TEXT_OBJ_SCOPES',
    'TEXT_OBJ_TYPES',
    'MAX_VIM_COUNT',
    'create_initial_vim_state',
    'create_initial_persistent_state',
    'is_operator_key',
    'is_text_obj_scope_key',
    'OperatorContext',
]