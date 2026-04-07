"""Sed edit parser matching src/tools/BashTool/sedEditParser.ts"""
import re
from typing import Dict, Any, List, Optional, Tuple


class SedEditParser:
    """Parser for sed edit commands."""

    # Pattern for sed substitution: s/old/new/flags
    SUBSTITUTION_PATTERN = re.compile(r's/([^/]*)/([^/]*)/([gimsuvwxy]*)')

    # Pattern for sed delete: nd or /pattern/d
    DELETE_PATTERN = re.compile(r'(\d+|/[^/]+/)d')

    # Pattern for sed insert/append: i\ or a\
    INSERT_PATTERN = re.compile(r'([ia])\\')

    @staticmethod
    def parse_substitution(command: str) -> Optional[Tuple[str, str, str]]:
        """Parse sed substitution command."""
        match = SedEditParser.SUBSTITUTION_PATTERN.search(command)
        if match:
            return (match.group(1), match.group(2), match.group(3))
        return None

    @staticmethod
    def parse_delete(command: str) -> Optional[str]:
        """Parse sed delete command."""
        match = SedEditParser.DELETE_PATTERN.search(command)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def parse(command: str) -> Dict[str, Any]:
        """Parse sed command."""
        result = {"type": "unknown", "valid": False}

        # Try substitution
        sub = SedEditParser.parse_substitution(command)
        if sub:
            result = {"type": "substitution", "valid": True, "old": sub[0], "new": sub[1], "flags": sub[2]}
            return result

        # Try delete
        delete = SedEditParser.parse_delete(command)
        if delete:
            result = {"type": "delete", "valid": True, "target": delete}
            return result

        return result


def parse_sed_edit(command: str) -> Dict[str, Any]:
    """Parse a sed edit command."""
    return SedEditParser.parse(command)


__all__ = ["SedEditParser", "parse_sed_edit"]