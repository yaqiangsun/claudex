"""Setup and initialization for Claude Code."""
import os
import sys
from typing import Optional, Dict, Any


def get_version() -> str:
    """Get Claude Code version."""
    return "0.1.0"


def get_platform_info() -> Dict[str, Any]:
    """Get platform information."""
    return {
        'os': os.name,
        'platform': sys.platform,
        'python_version': sys.version,
    }


def setup_environment() -> None:
    """Setup environment variables and paths."""
    # Set default environment variables
    if 'CLAUDE_HOME' not in os.environ:
        os.environ['CLAUDE_HOME'] = os.path.expanduser('~/.claude')


def check_dependencies() -> bool:
    """Check if all required dependencies are installed."""
    required = ['anthropic', 'click', 'pydantic', 'rich']
    for mod in required:
        try:
            __import__(mod)
        except ImportError:
            return False
    return True


def initialize() -> Dict[str, Any]:
    """Initialize Claude Code."""
    setup_environment()
    return {
        'version': get_version(),
        'platform': get_platform_info(),
        'dependencies_ok': check_dependencies(),
    }


__all__ = [
    'get_version',
    'get_platform_info',
    'setup_environment',
    'check_dependencies',
    'initialize',
]