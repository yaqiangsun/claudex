"""Memory paths."""
import os


def get_auto_mem_path() -> str:
    """Get auto memory path."""
    home = os.path.expanduser('~')
    return os.path.join(home, '.claude', 'projects', 'memory')


def get_team_mem_path() -> str:
    """Get team memory path."""
    return os.path.join(get_auto_mem_path(), 'team')


def is_auto_memory_enabled() -> bool:
    """Check if auto memory is enabled."""
    # TODO: implement with settings
    return True


__all__ = ['get_auto_mem_path', 'get_team_mem_path', 'is_auto_memory_enabled']