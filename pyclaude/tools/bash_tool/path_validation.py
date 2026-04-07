"""Path validation matching src/tools/BashTool/pathValidation.ts"""
import os
import re
from typing import Dict, Any, List, Optional


# Paths that should be protected
PROTECTED_PATHS = [
    '/etc/passwd',
    '/etc/shadow',
    '/etc/sudoers',
    '/etc/group',
    '/etc/hosts',
    '/etc/fstab',
    '/dev/',
    '/sys/',
    '/proc/',
    '/boot/',
    '/root/.ssh/',
]


# Patterns that indicate path traversal
PATH_TRAVERSAL_PATTERNS = [
    r'\.\.\/',
    r'\.\.$',
    r'\.\./',
    r'~\/[^/]*\.\.',
]


def is_protected_path(path: str) -> bool:
    """Check if path is protected."""
    abs_path = os.path.abspath(os.path.expanduser(path))

    for protected in PROTECTED_PATHS:
        if abs_path.startswith(protected):
            return True

    return False


def has_path_traversal(command: str) -> bool:
    """Check if command contains path traversal attempts."""
    for pattern in PATH_TRAVERSAL_PATTERNS:
        if re.search(pattern, command):
            return True
    return False


def validate_paths(command: str) -> Dict[str, Any]:
    """Validate paths in command."""
    warnings = []

    # Extract potential paths from command
    path_pattern = r'(?:^|\s)([~/][^\s]*)'
    paths = re.findall(path_pattern, command)

    for path in paths:
        if is_protected_path(path):
            warnings.append(f"Protected path: {path}")

    if has_path_traversal(command):
        warnings.append("Path traversal detected")

    return {
        "valid": len(warnings) == 0,
        "warnings": warnings,
    }


__all__ = ["PROTECTED_PATHS", "is_protected_path", "has_path_traversal", "validate_paths"]