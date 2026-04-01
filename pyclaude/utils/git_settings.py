"""
Git-related behaviors that depend on user settings.

This lives outside git.py because git.py is in the vscode extension's
dep graph and must stay free of settings.ts, which transitively pulls
opentelemetry. It's also a cycle: settings → git/gitignore → git → settings.
"""

import os


def should_include_git_instructions() -> bool:
    """Check if git instructions should be included in prompts."""
    env_val = os.environ.get("CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS")

    if env_val is not None and env_val.lower() in ("false", "0", ""):
        return True
    if env_val is not None and env_val.lower() in ("true", "1"):
        return False

    # Default to True if not set
    return True


__all__ = ["should_include_git_instructions"]