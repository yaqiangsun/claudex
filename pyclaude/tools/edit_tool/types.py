"""Types for EditTool matching src/tools/FileEditTool/types.ts"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class EditType(str, Enum):
    """Types of edits."""
    REPLACE = "replace"
    INSERT = "insert"
    DELETE = "delete"


@dataclass
class EditRange:
    """Range for edit operation."""
    start_line: int
    end_line: int


@dataclass
class EditOperation:
    """An edit operation."""
    edit_type: EditType
    path: str
    old_string: str
    new_string: str
    range: Optional[EditRange] = None


def validate_edit(edit: EditOperation) -> Dict[str, Any]:
    """Validate an edit operation."""
    errors = []

    if not edit.path:
        errors.append("Path is required")

    if edit.edit_type == EditType.REPLACE:
        if not edit.old_string:
            errors.append("old_string is required for replace")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


__all__ = ["EditType", "EditRange", "EditOperation", "validate_edit"]