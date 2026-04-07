"""Constants for ConfigTool matching src/tools/ConfigTool/constants.ts"""

# Config file locations
DEFAULT_CONFIG_PATH = "~/.config/pyclaude/settings.json"
DEFAULT_LOCAL_CONFIG = ".claude/settings.json"

# Config categories
CATEGORIES = [
    "general",
    "appearance",
    "tools",
    "hooks",
    "mcp",
    "permissions",
]

# Valid config keys
VALID_KEYS = [
    "autoApprove",
    "model",
    "maxTokens",
    "temperature",
    "theme",
    "fontSize",
    "terminalShell",
    "allowedDirectories",
    "blockedDirectories",
    "enableMcp",
    "enableHooks",
]


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "DEFAULT_LOCAL_CONFIG",
    "CATEGORIES",
    "VALID_KEYS",
]