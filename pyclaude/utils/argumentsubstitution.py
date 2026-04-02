"""
Argument substitution utility.

Handle argument substitution in commands.
"""

import re
from typing import Dict, Any, Optional


def substitute_arguments(command: str, args: Dict[str, Any]) -> str:
    """Substitute arguments in command string."""
    result = command
    for key, value in args.items():
        placeholder = f'{{{key}}}'
        result = result.replace(placeholder, str(value))
    return result


def parse_argument_placeholder(text: str) -> Optional[str]:
    """Parse argument placeholder from text."""
    match = re.search(r'\{(\w+)\}', text)
    return match.group(1) if match else None


def extract_placeholders(text: str) -> list:
    """Extract all placeholders from text."""
    return re.findall(r'\{(\w+)\}', text)


__all__ = ['substitute_arguments', 'parse_argument_placeholder', 'extract_placeholders']