"""Init command - initialize a project with CLAUDE.md."""

import os
from pathlib import Path
from typing import Any, Dict


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the init command."""
    cwd = os.getcwd()
    claude_md_path = Path(cwd) / 'CLAUDE.md'

    if claude_md_path.exists():
        return {
            'type': 'text',
            'value': 'CLAUDE.md already exists. Would you like me to review and improve it?',
        }

    # Generate initial CLAUDE.md
    content = """# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

[Describe your project here]

## Common Commands

- Build: [command]
- Test: [command]
- Lint: [command]

## Architecture

[Describe your project architecture]
"""

    return {
        'type': 'prompt',
        'prompt': f"""Please analyze this codebase and create a CLAUDE.md file with:
1. Common commands (build, test, lint)
2. Project architecture overview
3. Any special setup instructions

Current directory: {cwd}""",
    }


# Command metadata
CONFIG = {
    'type': 'prompt',
    'name': 'init',
    'description': 'Initialize project with CLAUDE.md',
}


call = execute  # Alias for compatibility