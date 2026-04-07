"""Simplify Skill - Python implementation of src/skills/bundled/simplify.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


SIMPLIFY_PROMPT = """# Simplify: Code Review and Cleanup

Review all changed files for reuse, quality, and efficiency. Fix any issues found.

## Phase 1: Identify Changes

Run `git diff` (or `git diff HEAD` if staged) to see what changed.

## Phase 2: Launch Three Review Agents in Parallel

### Agent 1: Code Reuse Review
- Search for existing utilities that could replace newly written code
- Flag any new function that duplicates existing functionality
- Flag inline logic that could use an existing utility

### Agent 2: Code Quality Review
- Redundant state or cached values that could be derived
- Parameter sprawl
- Copy-paste with slight variation
- Leaky abstractions
- Stringly-typed code
- Unnecessary comments

### Agent 3: Efficiency Review
- Unnecessary work or redundant computations
- Missed concurrency
- Hot-path bloat
- Unnecessary existence checks
- Memory issues

## Phase 3: Fix Issues

Wait for all agents to complete. Fix each issue directly.
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get simplify skill prompt."""
    prompt = SIMPLIFY_PROMPT
    if args:
        prompt += f'\n\n## Additional Focus\n\n{args}'
    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the simplify skill."""
    register_bundled_skill(BundledSkillDefinition(
        name='simplify',
        description='Review changed code for reuse, quality, and efficiency, then fix issues.',
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))