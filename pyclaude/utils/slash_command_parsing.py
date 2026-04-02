"""
Slash command parsing utility.
"""
import re
from typing import Optional, Tuple

def parse_slash_command(text: str) -> Optional[Tuple[str, str]]:
    match = re.match(r'^/(\w+)\s*(.*)$', text)
    if match:
        return match.group(1), match.group(2)
    return None

__all__ = ['parse_slash_command']