"""Commands package."""

from typing import Any, Dict

# Import command modules
from .help import call as help_call, AVAILABLE_COMMANDS
from .clear import call as clear_call
from .compact import call as compact_call, is_enabled as compact_enabled
from .commit import call as commit_call, CONFIG as COMMIT_CONFIG
from .resume import call as resume_call
from .version import call as version_call
from .status import call as status_call
from .btw import call as btw_call
from .init import call as init_call

# Command registry
COMMANDS: Dict[str, Any] = {
    'help': {'call': help_call, 'description': 'Show help'},
    'clear': {'call': clear_call, 'description': 'Clear conversation'},
    'compact': {'call': compact_call, 'description': 'Compact conversation'},
    'commit': {'call': commit_call, 'description': 'Create git commit'},
    'resume': {'call': resume_call, 'description': 'Resume session'},
    'version': {'call': version_call, 'description': 'Show version'},
    'status': {'call': status_call, 'description': 'Show session status'},
    'btw': {'call': btw_call, 'description': 'Add side note'},
    'init': {'call': init_call, 'description': 'Initialize project'},
}

def get_all_commands() -> list:
    """Get all available commands."""
    return list(COMMANDS.values())


__all__ = [
    # Local commands
    'COMMANDS',
    'get_all_commands',
    'help_call',
    'clear_call',
    'compact_call',
    'commit_call',
    'resume_call',
    'version_call',
    'status_call',
    'btw_call',
    'init_call',
    'AVAILABLE_COMMANDS',
]