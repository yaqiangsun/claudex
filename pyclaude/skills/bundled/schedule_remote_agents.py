"""Schedule Remote Agents Skill - Python implementation of src/skills/bundled/scheduleRemoteAgents.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


SCHEDULE_PROMPT = """# Schedule Remote Agents

You are helping the user schedule, update, list, or run **remote** Claude Code agents.

## What You Can Do
- list - list all triggers
- get - fetch one trigger
- create - create a trigger
- update - partial update
- run - run a trigger now

## Create body shape
```json
{
  "name": "AGENT_NAME",
  "cron_expression": "CRON_EXPR",
  "enabled": true,
  "job_config": {
    "ccr": {
      "environment_id": "ENVIRONMENT_ID",
      "session_context": {
        "model": "claude-sonnet-4-6",
        "sources": [{"git_repository": {"url": "https://github.com/ORG/REPO"}}],
        "allowed_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
      }
    }
  }
}
```

## Cron Expression Examples
- `0 9 * * 1-5` — Every weekday at 9am UTC
- `0 */2 * * *` — Every 2 hours
- `0 0 * * *` — Daily at midnight UTC

Minimum interval is 1 hour.

## Workflow

### CREATE
1. Understand the goal
2. Craft the prompt
3. Set the schedule
4. Choose the model
5. Review and confirm
6. Create via RemoteTriggerTool

### UPDATE
1. List triggers first
2. Ask what to change
3. Confirm and update

### LIST
1. Fetch and display
2. Show: name, schedule, enabled, next run

### RUN NOW
1. List if not specified
2. Confirm
3. Execute
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get schedule skill prompt."""
    prompt = SCHEDULE_PROMPT
    if args:
        prompt += f'\n## User Request\n\n{args}'
    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the schedule skill for remote agents."""
    # Note: is_enabled would check feature flags in full implementation
    register_bundled_skill(BundledSkillDefinition(
        name='schedule',
        description='Create, update, list, or run scheduled remote agents.',
        when_to_use='When the user wants to schedule a recurring remote agent or manage triggers.',
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))