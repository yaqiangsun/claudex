"""Skills command - manage skills."""

import os
import json
from pathlib import Path
from typing import Any, Dict, List


SKILLS_DIR = Path.home() / '.claude' / 'skills'


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the skills command."""
    args = args.strip().lower() if args else ''

    if not args or args == 'list':
        return await list_skills()

    if args == 'installed':
        return await list_skills()

    if args.startswith('enable '):
        skill_name = args[7:].strip()
        return await enable_skill(skill_name)

    if args.startswith('disable '):
        skill_name = args[8:].strip()
        return await disable_skill(skill_name)

    return {'type': 'text', 'value': '''Usage: /skills [command]

Commands:
  list              - List available skills
  enable <name>     - Enable a skill
  disable <name>    - Disable a skill
'''}


async def list_skills() -> Dict[str, Any]:
    """List available skills."""
    if not SKILLS_DIR.exists():
        return {'type': 'text', 'value': 'No skills installed. Skills are stored in ~/.claude/skills/'}

    skills = []
    for d in SKILLS_DIR.iterdir():
        if d.is_dir():
            skills.append(d.name)

    if not skills:
        return {'type': 'text', 'value': 'No skills installed.'}

    lines = ['Available skills:']
    for s in skills:
        lines.append(f'  /{s}')

    return {'type': 'text', 'value': '\n'.join(lines)}


async def enable_skill(name: str) -> Dict[str, Any]:
    """Enable a skill."""
    return {'type': 'text', 'value': f'Enabling skill: {name}... (not implemented)'}


async def disable_skill(name: str) -> Dict[str, Any]:
    """Disable a skill."""
    return {'type': 'text', 'value': f'Disabling skill: {name}... (not implemented)'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'skills',
    'description': 'Manage skills',
    'supports_non_interactive': True,
}


call = execute