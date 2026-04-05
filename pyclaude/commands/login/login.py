"""Login command - authenticate with Claude API."""

import os
from typing import Any, Dict


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the login command."""
    args = args.strip().lower() if args else ''

    if args == 'status':
        return await check_login_status()

    if args == 'logout':
        return await logout()

    # Ask for API key
    return {'type': 'text', 'value': '''Login to Claude Code

You can set your API key using:
  export ANTHROPIC_API_KEY=your_api_key

Or add it to ~/.claude/settings.json:
  {"api_key": "your_api_key"}

To check your login status, use: /login status
'''}


async def check_login_status() -> Dict[str, Any]:
    """Check login status."""
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')

    if api_key:
        # Mask most of the key
        masked = api_key[:7] + '*' * (len(api_key) - 10) + api_key[-3:] if len(api_key) > 10 else '***'
        return {'type': 'text', 'value': f'Logged in. API key: {masked}'}

    # Check settings file
    from ...commands.config.config import get_settings
    settings = get_settings()
    if settings.get('api_key'):
        return {'type': 'text', 'value': 'Logged in (API key from settings).'}

    return {'type': 'text', 'value': 'Not logged in. Use /login to set up your API key.'}


async def logout() -> Dict[str, Any]:
    """Logout."""
    # Remove from environment
    if 'ANTHROPIC_API_KEY' in os.environ:
        del os.environ['ANTHROPIC_API_KEY']

    # Remove from settings
    from ...commands.config.config import get_settings, save_settings
    settings = get_settings()
    if 'api_key' in settings:
        del settings['api_key']
        save_settings(settings)

    return {'type': 'text', 'value': 'Logged out.'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'login',
    'description': 'Authenticate with Claude API',
    'supports_non_interactive': True,
}


call = execute