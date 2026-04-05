"""Context management for Claude Code."""
import os
from functools import lru_cache
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


# Maximum status characters
MAX_STATUS_CHARS = 2000

# System prompt injection for cache breaking
_system_prompt_injection: Optional[str] = None


def get_system_prompt_injection() -> Optional[str]:
    """Get system prompt injection."""
    return _system_prompt_injection


def set_system_prompt_injection(value: Optional[str]) -> None:
    """Set system prompt injection and clear caches."""
    global _system_prompt_injection
    _system_prompt_injection = value
    # Clear context caches
    get_user_context.cache_clear()
    get_system_context.cache_clear()
    get_git_status.cache_clear()


@lru_cache(maxsize=1)
def get_git_status() -> Optional[str]:
    """Get git status for current directory."""
    from .utils.git import get_branch, get_default_branch, is_git
    from .utils.exec_file_no_throw import exec_file_no_throw
    from .utils.git import git_exe

    if not is_git():
        return None

    try:
        branch = get_branch()
        main_branch = get_default_branch()
        status_result = exec_file_no_throw(
            git_exe(),
            ['--no-optional-locks', 'status', '--short'],
            preserve_output_on_error=False,
        )
        status = status_result.get('stdout', '').strip() if status_result.get('success') else ''

        log_result = exec_file_no_throw(
            git_exe(),
            ['--no-optional-locks', 'log', '--oneline', '-n', '5'],
            preserve_output_on_error=False,
        )
        log = log_result.get('stdout', '').strip() if log_result.get('success') else ''

        name_result = exec_file_no_throw(
            git_exe(),
            ['config', 'user.name'],
            preserve_output_on_error=False,
        )
        user_name = name_result.get('stdout', '').strip() if name_result.get('success') else ''

        # Check if status exceeds character limit
        truncated_status = (
            status[:MAX_STATUS_CHARS] +
            '\n... (truncated because it exceeds 2k characters. If you need more information, run "git status" using BashTool)'
            if len(status) > MAX_STATUS_CHARS
            else status
        )

        parts = [
            'This is the git status at the start of the conversation. Note that this status is a snapshot in time, and will not update during the conversation.',
            f'Current branch: {branch}',
            f'Main branch (you will usually use this for PRs): {main_branch}',
        ]

        if user_name:
            parts.append(f'Git user: {user_name}')

        if truncated_status:
            parts.append(f'\n{truncated_status}')

        if log:
            parts.append(f'\nRecent commits:\n{log}')

        return '\n'.join(parts)
    except Exception:
        return None


@lru_cache(maxsize=1)
def get_user_context() -> Dict[str, Any]:
    """Get user context information."""
    cwd = os.getcwd()

    # Get CLAUDE.md content
    claude_md_path = os.path.join(cwd, 'CLAUDE.md')
    claude_md_content = None
    if os.path.isfile(claude_md_path):
        try:
            with open(claude_md_path, 'r') as f:
                claude_md_content = f.read()
        except Exception:
            pass

    # Get memory files
    memory_files = _get_memory_files()

    return {
        'cwd': cwd,
        'git_status': get_git_status(),
        'claude_md': claude_md_content,
        'memory_files': memory_files,
    }


def _get_memory_files() -> List[Dict[str, str]]:
    """Get memory files for the project."""
    from .utils.claude_md import get_memory_files

    try:
        return get_memory_files()
    except Exception:
        return []


@lru_cache(maxsize=1)
def get_system_context() -> Dict[str, Any]:
    """Get system context information."""
    from .utils.platform import get_platform_info

    return {
        'platform': os.name,
        'platform_info': get_platform_info(),
    }


def get_cwd_context() -> Dict[str, Any]:
    """Get current working directory context."""
    cwd = os.getcwd()
    return {
        'cwd': cwd,
        'cwd_name': os.path.basename(cwd),
        'cwd_parent': os.path.dirname(cwd),
    }


@dataclass
class ContextSnapshot:
    """A snapshot of context at a point in time."""
    timestamp: str = field(default_factory=lambda: str(__import__('datetime').datetime.now()))
    cwd: str = ''
    git_status: Optional[str] = None
    system_prompt_injection: Optional[str] = None
    user_context: Dict[str, Any] = field(default_factory=dict)
    system_context: Dict[str, Any] = field(default_factory=dict)


def capture_context_snapshot() -> ContextSnapshot:
    """Capture a snapshot of current context."""
    return ContextSnapshot(
        cwd=os.getcwd(),
        git_status=get_git_status(),
        system_prompt_injection=get_system_prompt_injection(),
        user_context=get_user_context(),
        system_context=get_system_context(),
    )


__all__ = [
    'get_system_prompt_injection',
    'set_system_prompt_injection',
    'get_git_status',
    'get_user_context',
    'get_system_context',
    'get_cwd_context',
    'capture_context_snapshot',
    'ContextSnapshot',
    'MAX_STATUS_CHARS',
]