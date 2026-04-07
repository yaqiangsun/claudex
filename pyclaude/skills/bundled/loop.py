"""Loop Skill - Python implementation of src/skills/bundled/loop.ts"""
from __future__ import annotations
import re
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


DEFAULT_INTERVAL = '10m'

USAGE_MESSAGE = f"""Usage: /loop [interval] <prompt>

Run a prompt or slash command on a recurring interval.

Intervals: Ns, Nm, Nh, Nd (e.g. 5m, 30m, 2h, 1d).
If no interval specified, defaults to {DEFAULT_INTERVAL}.

Examples:
  /loop 5m /babysit-prs
  /loop 30m check the deploy
  /loop check the deploy (defaults to {DEFAULT_INTERVAL})
"""


def build_prompt(args: str) -> str:
    """Build the loop prompt by parsing the arguments."""
    trimmed = args.strip()
    if not trimmed:
        return USAGE_MESSAGE

    # Parse interval from input
    interval = DEFAULT_INTERVAL
    prompt = trimmed

    # Rule 1: Leading token matches ^\\d+[smhd]$
    match = re.match(r'^(\d+[smhd])\s+(.*)$', trimmed)
    if match:
        interval = match.group(1)
        prompt = match.group(2)
    else:
        # Rule 2: Trailing "every" clause
        every_match = re.search(r'\s+every\s+(\d+)\s*(m(?:inute)?s?|h(?:our)?s?|d(?:ays?)?)$', trimmed, re.IGNORECASE)
        if every_match:
            num = every_match.group(1)
            unit = every_match.group(2).lower()
            if unit.startswith('m') and 'inute' not in unit:
                interval = f'{num}s'
            elif unit.startswith('m'):
                interval = f'{num}m'
            elif unit.startswith('h'):
                interval = f'{num}h'
            else:
                interval = f'{num}d'
            prompt = re.sub(r'\s+every\s+\d+\s*[smhdays]+\s*$', '', trimmed, flags=re.IGNORECASE).strip()

    return f"""# /loop — schedule a recurring prompt

## Parsed
- Interval: {interval}
- Prompt: {prompt}

## Action
1. Call CronCreate with the interval and prompt
2. Confirm what's scheduled, the cron expression, and how to cancel
3. Execute the prompt immediately

## Input
{args}
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get loop skill prompt."""
    trimmed = args.strip()
    if not trimmed:
        return [{'type': 'text', 'text': USAGE_MESSAGE}]
    return [{'type': 'text', 'text': build_prompt(trimmed)}]


def register() -> None:
    """Register the loop skill."""
    # Note: is_enabled would check isKairosCronEnabled in full implementation
    register_bundled_skill(BundledSkillDefinition(
        name='loop',
        description='Run a prompt or slash command on a recurring interval.',
        when_to_use='When the user wants to set up a recurring task or poll for status.',
        argument_hint='[interval] <prompt>',
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))