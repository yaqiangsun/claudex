"""Plugin types."""
from typing import Any, TypedDict


class PluginManifest(TypedDict):
    """Plugin manifest."""

    name: str
    description: str
    version: str


class PluginAuthor(TypedDict):
    """Plugin author."""

    name: str
    url: str


class CommandMetadata(TypedDict):
    """Command metadata."""

    name: str
    description: str


class BuiltinPluginDefinition(TypedDict):
    """Definition for a built-in plugin."""

    name: str
    description: str
    version: str | None
    skills: list[Any] | None
    hooks: dict | None
    mcp_servers: dict | None
    is_available: callable | None
    default_enabled: bool | None


class PluginRepository(TypedDict):
    """Plugin repository."""

    url: str
    branch: str
    last_updated: str | None
    commit_sha: str | None


class PluginConfig(TypedDict):
    """Plugin configuration."""

    repositories: dict[str, PluginRepository]


class LoadedPlugin(TypedDict):
    """Loaded plugin."""

    name: str
    manifest: PluginManifest
    path: str
    source: str
    repository: str
    enabled: bool | None
    is_builtin: bool | None
    sha: str | None
    commands_path: str | None
    commands_paths: list[str] | None
    commands_metadata: dict[str, CommandMetadata] | None
    agents_path: str | None
    agents_paths: list[str] | None
    skills_path: str | None
    skills_paths: list[str] | None
    output_styles_path: str | None
    output_styles_paths: list[str] | None
    hooks_config: dict | None
    mcp_servers: dict | None
    lsp_servers: dict | None
    settings: dict[str, Any] | None


PluginComponent = str  # 'commands' | 'agents' | 'skills' | 'hooks' | 'output-styles'


class PluginLoadResult(TypedDict):
    """Plugin load result."""

    enabled: list[LoadedPlugin]
    disabled: list[LoadedPlugin]
    errors: list[dict]


def get_plugin_error_message(error: dict) -> str:
    """Get display message from plugin error."""
    error_type = error.get('type', '')

    messages = {
        'generic-error': error.get('error', ''),
        'path-not-found': f"Path not found: {error.get('path')} ({error.get('component')})",
        'git-auth-failed': f"Git authentication failed ({error.get('auth_type')}): {error.get('git_url')}",
        'git-timeout': f"Git {error.get('operation')} timeout: {error.get('git_url')}",
        'network-error': f"Network error: {error.get('url')}",
        'manifest-parse-error': f"Manifest parse error: {error.get('parse_error')}",
        'manifest-validation-error': f"Manifest validation failed: {error.get('validation_errors', [])}",
        'plugin-not-found': f"Plugin {error.get('plugin_id')} not found in marketplace {error.get('marketplace')}",
        'marketplace-not-found': f"Marketplace {error.get('marketplace')} not found",
        'marketplace-load-failed': f"Marketplace {error.get('marketplace')} failed to load: {error.get('reason')}",
        'mcp-config-invalid': f"MCP server {error.get('server_name')} invalid: {error.get('validation_error')}",
        'hook-load-failed': f"Hook load failed: {error.get('reason')}",
        'component-load-failed': f"{error.get('component')} load failed: {error.get('reason')}",
        'dependency-unsatisfied': f"Dependency '{error.get('dependency')}' is {error.get('reason')}",
    }

    return messages.get(error_type, f'Unknown error: {error_type}')


__all__ = [
    'PluginManifest',
    'PluginAuthor',
    'CommandMetadata',
    'BuiltinPluginDefinition',
    'PluginRepository',
    'PluginConfig',
    'LoadedPlugin',
    'PluginComponent',
    'PluginLoadResult',
    'get_plugin_error_message',
]