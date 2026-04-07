"""Read-only validation matching src/tools/BashTool/readOnlyValidation.ts"""
from typing import Dict, Any


# Commands that only read data
READ_ONLY_COMMANDS = [
    'cat', 'head', 'tail', 'less', 'more', 'grep', 'egrep', 'fgrep',
    'find', 'ls', 'll', 'la', 'stat', 'file', 'diff', 'comm',
    'git diff', 'git log', 'git show', 'git status', 'git blame',
    'which', 'whereis', 'type', 'command', 'hash',
    'env', 'printenv', 'set', 'export',
    'hostname', 'uname', 'whoami', 'id', 'groups',
    'df', 'du', 'free', 'top', 'ps', 'pstree',
]


# Patterns for commands that only read
READ_ONLY_PATTERNS = [
    r'^cat\s+',
    r'^head\s+',
    r'^tail\s+',
    r'^grep\s+',
    r'^find\s+',
    r'^ls\s+',
    r'^git\s+(diff|log|show|status|blame)',
]


def is_read_only_command(command: str) -> bool:
    """Check if command is read-only."""
    command = command.strip()

    # Check exact matches
    cmd_base = command.split()[0] if command else ""
    if cmd_base in READ_ONLY_COMMANDS:
        return True

    # Check patterns
    import re
    for pattern in READ_ONLY_PATTERNS:
        if re.match(pattern, command):
            return True

    return False


def validate_read_only(command: str, mode: str = "normal") -> Dict[str, Any]:
    """Validate command in read-only mode."""
    if mode != "read_only":
        return {"allowed": True, "read_only": False}

    return {
        "allowed": is_read_only_command(command),
        "read_only": True,
    }


__all__ = ["READ_ONLY_COMMANDS", "READ_ONLY_PATTERNS", "is_read_only_command", "validate_read_only"]