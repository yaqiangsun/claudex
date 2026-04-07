"""Destructive command warning matching src/tools/BashTool/destructiveCommandWarning.ts"""
import re
from typing import Dict, Any, List, Optional


DESTRUCTIVE_PATTERNS = [
    (r'rm\s+-rf?\s+', 'Recursive delete'),
    (r'rmdir\s+', 'Remove directory'),
    (r'del\s+', 'Delete command'),
    (r'>\s*/dev/', 'Write to device'),
    (r'>\s*/etc/', 'Write to system directory'),
    (r'dd\s+if=', 'Direct disk operation'),
    (r'mkfs\.', 'Filesystem format'),
    (r':\(\)\{.*:\|:', 'Fork bomb'),
    (r'sudo\s+rm', 'Sudo delete'),
    (r'sudo\s+rmdir', 'Sudo remove directory'),
    (r'chmod\s+-R\s+777', 'World-writable permissions'),
    (r'chown\s+-R', 'Recursive ownership change'),
    (r'drop\s+table', 'Database drop'),
    (r'drop\s+database', 'Database drop'),
    (r'truncate\s+', 'Truncate file'),
    (r'shred\s+', 'Secure delete'),
]


def check_destructive(command: str) -> Dict[str, Any]:
    """Check if command is destructive."""
    warnings = []

    for pattern, description in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            warnings.append(description)

    return {
        "is_destructive": len(warnings) > 0,
        "warnings": warnings,
        "requires_confirmation": len(warnings) > 0,
    }


def get_warning_message(command: str) -> Optional[str]:
    """Get warning message for destructive command."""
    result = check_destructive(command)
    if result["is_destructive"]:
        return f"Warning: This command may be destructive. ({', '.join(result['warnings'])})"
    return None


__all__ = ["DESTRUCTIVE_PATTERNS", "check_destructive", "get_warning_message"]