"""Diff command - show git diff."""

import subprocess
from typing import Any, Dict, Optional


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the diff command."""
    args = args.strip()

    # Build git diff command
    cmd = ['git', 'diff']

    if '--staged' in args or '-s' in args:
        cmd.append('--staged')
        args = args.replace('--staged', '').replace('-s', '')

    if '--stat' in args:
        cmd.append('--stat')
        args = args.replace('--stat', '')

    # Add any file arguments
    file_args = [a for a in args.split() if a and not a.startswith('-')]
    cmd.extend(file_args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )

        if not result.stdout and not result.stderr:
            return {'type': 'text', 'value': 'No changes.'}

        output = result.stdout or result.stderr
        return {'type': 'text', 'value': output}

    except Exception as e:
        return {'type': 'text', 'value': f'Error: {e}'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'diff',
    'description': 'Show git diff',
    'aliases': ['git diff'],
    'supports_non_interactive': True,
}


call = execute