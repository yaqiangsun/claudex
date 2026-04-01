"""Version command - print version info."""

import os
from typing import Any, Dict

__version__ = '1.0.0'  # Placeholder version


def is_enabled() -> bool:
    """Check if version command is enabled."""
    return os.environ.get('USER_TYPE') == 'ant'


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, str]:
    """Execute the version command."""
    return {
        'type': 'text',
        'value': __version__,
    }


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'version',
    'description': 'Print the version',
    'is_enabled': is_enabled,
    'supports_non_interactive': True,
}


call = execute  # Alias for compatibility