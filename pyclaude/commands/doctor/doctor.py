"""Doctor command - diagnose issues."""

import os
import sys
import subprocess
from pathlib import Path
from typing import Any, Dict, List


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the doctor command."""
    args = args.strip().lower() if args else ''

    issues = []
    checks = []

    # Check Python version
    checks.append(('Python version', f'{sys.version.split()[0]}', True))

    # Check API key
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    has_api_key = bool(api_key)
    checks.append(('ANTHROPIC_API_KEY', 'Set' if has_api_key else 'Not set', has_api_key))

    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        node_version = result.stdout.strip() if result.returncode == 0 else 'Not found'
        checks.append(('Node.js', node_version, result.returncode == 0))
    except Exception:
        checks.append(('Node.js', 'Not found', False))

    # Check git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        git_version = result.stdout.strip() if result.returncode == 0 else 'Not found'
        checks.append(('Git', git_version, result.returncode == 0))
    except Exception:
        checks.append(('Git', 'Not found', False))

    # Check Claude settings
    settings_file = Path.home() / '.claude' / 'settings.json'
    has_settings = settings_file.exists()
    checks.append(('Claude settings', 'Present' if has_settings else 'Missing', has_settings))

    # Build output
    lines = ['Claude Code Doctor', '=' * 40]

    for name, value, passed in checks:
        status = '✓' if passed else '✗'
        lines.append(f'{status} {name}: {value}')
        if not passed:
            issues.append(name)

    lines.append('')
    if issues:
        lines.append(f'Issues found: {", ".join(issues)}')
    else:
        lines.append('All checks passed!')

    return {'type': 'text', 'value': '\n'.join(lines)}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'doctor',
    'description': 'Diagnose Claude Code issues',
    'aliases': ['diagnose', 'check'],
    'supports_non_interactive': True,
}


call = execute