"""Supported settings for ConfigTool matching src/tools/ConfigTool/supportedSettings.ts"""
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class SettingDefinition:
    """Definition of a configuration setting."""
    key: str
    type: str
    default: Any
    description: str
    required: bool = False


# All supported settings
SUPPORTED_SETTINGS: Dict[str, SettingDefinition] = {
    "autoApprove": SettingDefinition(
        key="autoApprove",
        type="boolean",
        default=False,
        description="Automatically approve safe commands",
    ),
    "model": SettingDefinition(
        key="model",
        type="string",
        default="claude-sonnet-4-6",
        description="Default model to use",
    ),
    "maxTokens": SettingDefinition(
        key="maxTokens",
        type="number",
        default=4096,
        description="Maximum tokens per response",
    ),
    "temperature": SettingDefinition(
        key="temperature",
        type="number",
        default=1.0,
        description="Model temperature",
    ),
    "theme": SettingDefinition(
        key="theme",
        type="string",
        default="dark",
        description="UI theme",
    ),
    "terminalShell": SettingDefinition(
        key="terminalShell",
        type="string",
        default="bash",
        description="Default shell to use",
    ),
}


def get_setting(key: str) -> SettingDefinition:
    """Get setting definition by key."""
    return SUPPORTED_SETTINGS.get(key)


def list_settings() -> List[str]:
    """List all available setting keys."""
    return list(SUPPORTED_SETTINGS.keys())


__all__ = ["SettingDefinition", "SUPPORTED_SETTINGS", "get_setting", "list_settings"]