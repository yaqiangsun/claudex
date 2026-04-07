"""Stuck Skill - Python implementation of src/skills/bundled/stuck.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill, is_ant_user


STUCK_PROMPT = """# /stuck — diagnose frozen/slow Claude Code sessions

The user thinks another Claude Code session on this machine is frozen, stuck, or slow.

## What to look for

- **High CPU (≥90%) sustained** - likely infinite loop
- **Process state D** - uninterruptible sleep, I/O hang
- **Process state T** - stopped (Ctrl+Z)
- **Process state Z** - zombie
- **Very high RSS (≥4GB)** - memory leak
- **Stuck child process** - hung git/node/etc

## Investigation steps

1. List all Claude Code processes:
   `ps -axo pid=,pcpu=,rss=,etime=,state=,comm= | grep -E '(claude|cli)'`

2. For suspicious processes:
   - Child processes: `pgrep -lP <pid>`
   - If high CPU: sample again after 1-2s
   - Check debug log if available

## Report

Only post if something stuck. If healthy, tell user directly.
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get stuck skill prompt."""
    prompt = STUCK_PROMPT
    if args:
        prompt += f'\n\n## User-provided context\n\n{args}'
    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the stuck skill (ANT-only)."""
    if not is_ant_user():
        return

    register_bundled_skill(BundledSkillDefinition(
        name='stuck',
        description='[ANT-ONLY] Investigate frozen/stuck/slow Claude Code sessions.',
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))