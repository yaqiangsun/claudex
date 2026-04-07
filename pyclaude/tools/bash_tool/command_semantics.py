"""Command semantics matching src/tools/BashTool/commandSemantics.ts"""
from typing import Dict, Any, List, Optional
import re


class CommandType:
    """Types of bash commands."""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    COMPOUND = "compound"
    UNKNOWN = "unknown"


COMMAND_PATTERNS = {
    CommandType.READ: [
        r'^cat\s+',
        r'^head\s+',
        r'^tail\s+',
        r'^less\s+',
        r'^more\s+',
        r'^grep\s+',
        r'^find\s+',
        r'^ls\s+',
        r'^stat\s+',
        r'^file\s+',
        r'^diff\s+',
        r'^git\s+diff',
        r'^git\s+log',
        r'^git\s+show',
        r'^git\s+status',
    ],
    CommandType.WRITE: [
        r'^rm\s+',
        r'^mv\s+',
        r'^cp\s+',
        r'^touch\s+',
        r'^mkdir\s+',
        r'^rmdir\s+',
        r'^chmod\s+',
        r'^chown\s+',
        r'^echo\s+>',
        r'^tee\s+',
        r'^sed\s+-i',
        r'^awk\s+-i',
    ],
    CommandType.EXECUTE: [
        r'^python',
        r'^node',
        r'^npm\s+',
        r'^pip\s+',
        r'^cargo\s+',
        r'^go\s+',
        r'^make\s+',
        r'^cmake\s+',
        r'^./',
        r'^bash\s+',
        r'^sh\s+',
    ],
}


def classify_command(command: str) -> str:
    """Classify the type of command."""
    command = command.strip()

    for cmd_type, patterns in COMMAND_PATTERNS.items():
        for pattern in patterns:
            if re.match(pattern, command, re.IGNORECASE):
                return cmd_type

    return CommandType.UNKNOWN


def get_command_intent(command: str) -> Dict[str, Any]:
    """Get the intent of a command."""
    cmd_type = classify_command(command)

    return {
        "type": cmd_type,
        "is_read": cmd_type == CommandType.READ,
        "is_write": cmd_type == CommandType.WRITE,
        "is_execute": cmd_type == CommandType.EXECUTE,
        "is_compound": "&&" in command or "||" in command or ";" in command,
    }


__all__ = ["CommandType", "classify_command", "get_command_intent"]