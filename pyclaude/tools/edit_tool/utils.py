"""Utils for EditTool matching src/tools/FileEditTool/utils.ts"""
import re
from typing import Dict, Any, List, Optional, Tuple


def find_line_range(content: str, old_string: str) -> Optional[Tuple[int, int]]:
    """Find line range for old_string in content."""
    if not old_string:
        return None

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if old_string in line:
            start = i + 1
            end = i + 1
            # Check multi-line
            if '\n' in old_string:
                for j in range(i + 1, len(lines)):
                    if old_string in '\n'.join(lines[i:j+1]):
                        end = j + 1
            return (start, end)
    return None


def apply_edit(content: str, old_string: str, new_string: str) -> str:
    """Apply an edit to content."""
    if old_string in content:
        return content.replace(old_string, new_string, 1)
    return content


def validate_edit_input(
    path: str,
    old_string: str,
    new_string: str,
) -> Dict[str, Any]:
    """Validate edit input."""
    errors = []
    warnings = []

    if not path:
        errors.append("Path is required")

    if not old_string and not new_string:
        errors.append("Either old_string or new_string must be provided")

    # Check for potentially dangerous edits
    if old_string == new_string:
        warnings.append("old_string and new_string are identical")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


__all__ = ["find_line_range", "apply_edit", "validate_edit_input"]