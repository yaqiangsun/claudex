"""Debug Skill - Python implementation of src/skills/bundled/debug.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get debug skill prompt."""
    prompt = f"""# Debug Skill

Help the user debug an issue they're encountering in this Claude Code session.

## Session Debug Log
Debug logs are at: ~/.claude/debug/

## Issue Description
{args or 'The user did not describe a specific issue.'}

## Instructions
1. Review the user's issue description
2. Look for error patterns
3. Explain what you found in plain language
4. Suggest concrete fixes or next steps
"""
    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the debug skill."""
    register_bundled_skill(BundledSkillDefinition(
        name='debug',
        description='Enable debug logging and help diagnose issues with Claude Code.',
        allowed_tools=['Read', 'Grep', 'Glob'],
        argument_hint='[issue description]',
        disable_model_invocation=True,
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))