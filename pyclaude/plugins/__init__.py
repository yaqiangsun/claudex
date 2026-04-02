"""Built-in Plugin Registry."""
from typing import Any

BUILTIN_MARKETPLACE_NAME = 'builtin'

# Global registry for built-in plugins
_BUILTIN_PLUGINS: dict[str, Any] = {}


def register_builtin_plugin(definition: dict) -> None:
    """Register a built-in plugin."""
    _BUILTIN_PLUGINS[definition['name']] = definition


def is_builtin_plugin_id(plugin_id: str) -> bool:
    """Check if plugin ID is a built-in plugin."""
    return plugin_id.endswith(f'@{BUILTIN_MARKETPLACE_NAME}')


def get_builtin_plugin_definition(name: str) -> dict | None:
    """Get a specific built-in plugin definition."""
    return _BUILTIN_PLUGINS.get(name)


def get_builtin_plugins() -> dict[str, list]:
    """Get all registered built-in plugins."""
    # TODO: implement with actual settings
    return {'enabled': [], 'disabled': []}


def get_builtin_plugin_skill_commands() -> list:
    """Get skills from enabled built-in plugins."""
    return []


def clear_builtin_plugins() -> None:
    """Clear built-in plugins registry."""
    _BUILTIN_PLUGINS.clear()


__all__ = [
    'BUILTIN_MARKETPLACE_NAME',
    'register_builtin_plugin',
    'is_builtin_plugin_id',
    'get_builtin_plugin_definition',
    'get_builtin_plugins',
    'get_builtin_plugin_skill_commands',
    'clear_builtin_plugins',
]