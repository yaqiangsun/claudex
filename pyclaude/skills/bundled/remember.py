"""Remember Skill - Python implementation of src/skills/bundled/remember.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import (
    BundledSkillDefinition,
    register_bundled_skill,
    is_auto_memory_enabled,
)


SKILL_PROMPT = """# Memory Review

## Goal
Review the user's memory landscape and produce a clear report of proposed changes. Do NOT apply changes.

## Steps

### 1. Gather all memory layers
Read CLAUDE.md and CLAUDE.local.md from the project root (if they exist).

### 2. Classify each auto-memory entry
| Destination | What belongs there |
|-------------|-------------------|
| CLAUDE.md | Project conventions for all contributors |
| CLAUDE.local.md | Personal instructions, not for others |
| Stay in auto-memory | Working notes, temporary context |

### 3. Identify cleanup opportunities
- Duplicates: entries already in CLAUDE.md → propose removing
- Outdated: entries contradicted by newer ones → propose update
- Conflicts: contradictions between layers → propose resolution

### 4: Present the report
Output grouped by action type:
1. Promotions - entries to move
2. Cleanup - duplicates, outdated, conflicts
3. Ambiguous - need user input
4. No action needed

## Rules
- Present ALL proposals before making changes
- Do NOT modify files without explicit user approval
- Ask about ambiguous entries
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get remember skill prompt."""
    prompt = SKILL_PROMPT
    if args:
        prompt += f'\n\n## Additional context\n\n{args}'
    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the remember skill."""
    register_bundled_skill(BundledSkillDefinition(
        name='remember',
        description='Review auto-memory entries and propose promotions to CLAUDE.md or CLAUDE.local.md.',
        when_to_use='Use when the user wants to review, organize, or promote their auto-memory entries.',
        user_invocable=True,
        is_enabled=is_auto_memory_enabled,
        get_prompt_for_command=get_prompt,
    ))