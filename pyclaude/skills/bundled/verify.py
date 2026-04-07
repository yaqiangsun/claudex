"""Verify Skill - Python implementation of src/skills/bundled/verify.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill, is_ant_user


VERIFY_PROMPT = """# Verify Skill

Verify a code change does what it should by running the app.

## Steps
1. Run `git diff` to see what changed
2. Review the changes for correctness
3. Run tests or verify the functionality works as expected
4. Report findings
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get verify skill prompt."""
    parts = [VERIFY_PROMPT.strip()]
    if args:
        parts.append(f'## User Request\n\n{args}')
    return [{'type': 'text', 'text': '\n\n'.join(parts)}]


def register() -> None:
    """Register the verify skill (ANT-only)."""
    if not is_ant_user():
        return

    register_bundled_skill(BundledSkillDefinition(
        name='verify',
        description='Verify a code change does what it should by running the app.',
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))