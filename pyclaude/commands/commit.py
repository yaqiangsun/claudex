"""Commit command - creates a git commit."""

import os
import subprocess
from typing import Any, Dict, List, Optional


ALLOWED_TOOLS = [
    'Bash(git add:*)',
    'Bash(git status:*)',
    'Bash(git commit:*)',
]


def get_prompt_content() -> str:
    """Get the prompt content for commit command."""
    return """## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Git Safety Protocol

- NEVER update the git config
- NEVER skip hooks (--no-verify, --no-gpg-sign, etc) unless the user explicitly requests it
- CRITICAL: ALWAYS create NEW commits. NEVER use git commit --amend, unless the user explicitly requests it
- Do not commit files that likely contain secrets (.env, credentials.json, etc). Warn the user if they specifically request to commit those files
- If there are no changes to commit (i.e., no untracked files and no modifications), do not create an empty commit
- Never use git commands with the -i flag (like git rebase -i or git add -i) since they require interactive input which is not supported

## Your task

Based on the above changes, create a single git commit:

1. Analyze all staged changes and draft a commit message:
   - Look at the recent commits above to follow this repository's commit message style
   - Summarize the nature of the changes (new feature, enhancement, bug fix, refactoring, test, docs, etc.)
   - Ensure the message accurately reflects the changes and their purpose
   - Draft a concise (1-2 sentences) commit message that focuses on the "why" rather than the "what"

2. Stage relevant files and create the commit using HEREDOC syntax

You have the capability to call multiple tools in a single response."""


def get_git_status() -> str:
    """Get current git status."""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout or ''
    except Exception as e:
        return f'Error: {e}'


def get_git_diff() -> str:
    """Get current git diff."""
    try:
        result = subprocess.run(
            ['git', 'diff', 'HEAD'],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout or ''
    except Exception as e:
        return f'Error: {e}'


def get_git_branch() -> str:
    """Get current git branch."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() or 'unknown'
    except Exception:
        return 'unknown'


def get_git_log() -> str:
    """Get recent git commits."""
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', '-10'],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout or ''
    except Exception:
        return ''


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the commit command."""
    # Check for staged changes
    status = get_git_status()
    if not status.strip():
        return {'type': 'error', 'value': 'No changes to commit'}

    # Return prompt-based command structure
    return {
        'type': 'prompt',
        'prompt': get_prompt_content(),
        'allowed_tools': ALLOWED_TOOLS,
        'progress_message': 'creating commit',
    }


# Command metadata
CONFIG = {
    'type': 'prompt',
    'name': 'commit',
    'description': 'Create a git commit',
    'allowed_tools': ALLOWED_TOOLS,
    'source': 'builtin',
}


call = execute  # Alias for compatibility