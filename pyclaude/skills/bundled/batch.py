"""Batch Skill - Python implementation of src/skills/bundled/batch.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


DEFAULT_INTERVAL = '10m'

WORKER_INSTRUCTIONS = """After you finish implementing the change:
1. Simplify - review and clean up changes
2. Run unit tests - fix if they fail
3. Test end-to-end
4. Commit and push - create a PR
5. Report - End with `PR: <url>` or `PR: none — <reason>`
"""


def build_prompt(instruction: str) -> str:
    """Build the batch prompt for the given instruction."""
    return f"""# Batch: Parallel Work Orchestration

You are orchestrating a large, parallelizable change across this codebase.

## User Instruction

{instruction}

## Phase 1: Research and Plan (Plan Mode)

1. **Understand the scope** - Launch subagents to research what this instruction touches
2. **Decompose into independent units** - 5-30 self-contained units
3. **Determine the e2e test recipe** - How to verify the change works
4. **Write the plan** - Include summary, work units, e2e recipe, worker instructions
5. Exit plan mode for approval

## Phase 2: Spawn Workers

Spawn background agents in isolated git worktrees. Each prompt must be fully self-contained.

## Phase 3: Track Progress

Render status table and update as agents complete.
"""


MISSING_INSTRUCTION = """Provide an instruction describing the batch change you want to make.

Examples:
  /batch migrate from react to vue
  /batch replace all uses of lodash with native equivalents"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get batch skill prompt."""
    instruction = args.strip()
    if not instruction:
        return [{'type': 'text', 'text': MISSING_INSTRUCTION}]
    return [{'type': 'text', 'text': build_prompt(instruction)}]


def register() -> None:
    """Register the batch skill."""
    register_bundled_skill(BundledSkillDefinition(
        name='batch',
        description='Research and plan a large-scale change, then execute in parallel across 5-30 worktree agents.',
        when_to_use='Use when the user wants to make a sweeping, mechanical change across many files.',
        argument_hint='<instruction>',
        user_invocable=True,
        disable_model_invocation=True,
        get_prompt_for_command=get_prompt,
    ))