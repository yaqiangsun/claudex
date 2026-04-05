"""Model command - switch between Claude models."""

import os
from typing import Any, Dict, List


AVAILABLE_MODELS = [
    'claude-opus-4-6-20250514',
    'claude-sonnet-4-20250514',
    'claude-haiku-4-5-20250501',
]


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the model command."""
    args = args.strip().lower() if args else ''

    if not args or args == 'list':
        return await list_models()

    if args == 'current':
        return await show_current_model()

    # Try to set a model
    model = args
    if model not in AVAILABLE_MODELS:
        # Try with prefix
        for m in AVAILABLE_MODELS:
            if model in m:
                model = m
                break
        else:
            return {'type': 'text', 'value': f'Unknown model: {args}\n\nAvailable models:\n  ' + '\n  '.join(AVAILABLE_MODELS)}

    return await set_model(model)


async def list_models() -> Dict[str, Any]:
    """List available models."""
    current = os.environ.get('CLAUDE_MODEL', '')

    lines = ['Available models:']
    for m in AVAILABLE_MODELS:
        marker = ' (current)' if m == current else ''
        lines.append(f'  {m}{marker}')

    return {'type': 'text', 'value': '\n'.join(lines)}


async def show_current_model() -> Dict[str, Any]:
    """Show current model."""
    model = os.environ.get('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
    return {'type': 'text', 'value': f'Current model: {model}'}


async def set_model(model: str) -> Dict[str, Any]:
    """Set the model."""
    os.environ['CLAUDE_MODEL'] = model
    return {'type': 'text', 'value': f'Switched to model: {model}'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'model',
    'description': 'Switch between Claude models',
    'supports_non_interactive': True,
}


call = execute