"""Skillify Skill - Python implementation of src/skills/bundled/skillify.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill, is_ant_user


SKILLIFY_PROMPT = """# Skillify

Capture this session's repeatable process into a reusable skill.

## Your Task

### Step 1: Analyze the Session
- What repeatable process was performed
- What the inputs/parameters were
- The distinct steps (in order)
- What tools and permissions were needed

### Step 2: Interview the User
Use AskUserQuestion to understand:
- Name and description for the skill
- High-level goals and success criteria
- Steps involved
- Where to save (repo vs user)
- Arguments if needed
- Trigger phrases

### Step 3: Write the SKILL.md
Create at the location chosen in Step 2.

Format:
```markdown
---
name: {{skill-name}}
description: {{one-line description}}
allowed-tools: {{list of tool permissions}}
when_to_use: {{when to auto-invoke}}
argument-hint: "{{hint}}"
arguments: {{arg names}}
---

# Skill Title
Description

## Inputs
- `$arg_name`: Description

## Goal
Goal statement

## Steps

### 1. Step Name
What to do
**Success criteria**: What proves this step is done
```
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get skillify skill prompt."""
    prompt = SKILLIFY_PROMPT
    if args:
        prompt += f'\n\nThe user described this process as: "{args}"'
    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the skillify skill (ANT-only)."""
    if not is_ant_user():
        return

    register_bundled_skill(BundledSkillDefinition(
        name='skillify',
        description="Capture this session's repeatable process into a skill.",
        allowed_tools=['Read', 'Write', 'Edit', 'Glob', 'Grep', 'AskUserQuestion'],
        user_invocable=True,
        disable_model_invocation=True,
        argument_hint='[description of the process]',
        get_prompt_for_command=get_prompt,
    ))