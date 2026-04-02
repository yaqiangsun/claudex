"""
CLI argument parsing utilities.

Python adaptation.
"""

import sys
from typing import Optional, Tuple, List


def eager_parse_cli_flag(flag_name: str, argv: Optional[List[str]] = None) -> Optional[str]:
    """Parse a CLI flag value early, before Commander.js processes arguments.

    Supports both space-separated (--flag value) and equals-separated (--flag=value) syntax.

    Args:
        flag_name: The flag name including dashes (e.g., '--settings')
        argv: Optional argv array to parse (defaults to sys.argv)

    Returns:
        The value if found, None otherwise
    """
    if argv is None:
        argv = sys.argv

    for i, arg in enumerate(argv):
        # Handle --flag=value syntax
        if arg and arg.startswith(f"{flag_name}="):
            return arg[len(flag_name) + 1 :]
        # Handle --flag value syntax
        if arg == flag_name and i + 1 < len(argv):
            return argv[i + 1]

    return None


def extract_args_after_double_dash(
    command_or_value: str,
    args: Optional[List[str]] = None,
) -> Tuple[str, List[str]]:
    """Handle the standard Unix '--' separator convention in CLI arguments.

    When using a CLI parser with pass-through options, the '--' separator
    is passed through as a positional argument rather than being consumed.

    Args:
        command_or_value: The parsed positional that may be "--"
        args: The remaining arguments array

    Returns:
        Tuple of (command, args)
    """
    if args is None:
        args = []

    if command_or_value == "--" and len(args) > 0:
        return (args[0], args[1:])
    return (command_or_value, args)


__all__ = [
    "eager_parse_cli_flag",
    "extract_args_after_double_dash",
]