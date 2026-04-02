"""
Environment utilities.

Python adaptation.
"""

import os
import sys
from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=1)
def get_claude_config_home_dir() -> str:
    """Get Claude config home directory."""
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
    if config_dir:
        return str(Path(config_dir).normalize())
    return str(Path.home() / ".claude")


def get_teams_dir() -> str:
    """Get teams directory."""
    return os.path.join(get_claude_config_home_dir(), "teams")


def has_node_option(flag: str) -> bool:
    """Check if NODE_OPTIONS contains a specific flag."""
    node_options = os.environ.get("NODE_OPTIONS")
    if not node_options:
        return False
    return flag in node_options.split()


def is_env_truthy(env_var) -> bool:
    """Check if environment variable is truthy."""
    if not env_var:
        return False
    if isinstance(env_var, bool):
        return env_var
    normalized_value = str(env_var).lower().strip()
    return normalized_value in ("1", "true", "yes", "on")


def is_env_defined_falsy(env_var) -> bool:
    """Check if environment variable is defined but falsy."""
    if env_var is None:
        return False
    if isinstance(env_var, bool):
        return not env_var
    if not env_var:
        return False
    normalized_value = str(env_var).lower().strip()
    return normalized_value in ("0", "false", "no", "off")


def is_bare_mode() -> bool:
    """Check if running in bare mode (--bare)."""
    return is_env_truthy(os.environ.get("CLAUDE_CODE_SIMPLE")) or "--bare" in sys.argv


def parse_env_vars(raw_env_args):
    """Parse array of environment variable strings into key-value object."""
    parsed_env = {}

    if raw_env_args:
        for env_str in raw_env_args:
            parts = env_str.split("=", 1)
            if not parts[0] or len(parts) < 2:
                raise ValueError(
                    f"Invalid environment variable format: {env_str}, "
                    "environment variables should be added as: -e KEY1=value1 -e KEY2=value2"
                )
            parsed_env[parts[0]] = parts[1]

    return parsed_env


def get_aws_region() -> str:
    """Get AWS region with fallback."""
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def get_default_vertex_region() -> str:
    """Get default Vertex AI region."""
    return os.environ.get("CLOUD_ML_REGION", "us-east5")


def should_maintain_project_working_dir() -> bool:
    """Check if bash commands should maintain project working directory."""
    return is_env_truthy(os.environ.get("CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR"))


def is_running_on_homespace() -> bool:
    """Check if running on Homespace (ant-internal cloud environment)."""
    return os.environ.get("USER_TYPE") == "ant" and is_env_truthy(
        os.environ.get("COO_RUNNING_ON_HOMESPACE")
    )


# Vertex region overrides by model prefix
_VERTEX_REGION_OVERRIDES = [
    ("claude-haiku-4-5", "VERTEX_REGION_CLAUDE_HAIKU_4_5"),
    ("claude-3-5-haiku", "VERTEX_REGION_CLAUDE_3_5_HAIKU"),
    ("claude-3-5-sonnet", "VERTEX_REGION_CLAUDE_3_5_SONNET"),
    ("claude-3-7-sonnet", "VERTEX_REGION_CLAUDE_3_7_SONNET"),
    ("claude-opus-4-1", "VERTEX_REGION_CLAUDE_4_1_OPUS"),
    ("claude-opus-4", "VERTEX_REGION_CLAUDE_4_0_OPUS"),
    ("claude-sonnet-4-6", "VERTEX_REGION_CLAUDE_4_6_SONNET"),
    ("claude-sonnet-4-5", "VERTEX_REGION_CLAUDE_4_5_SONNET"),
    ("claude-sonnet-4", "VERTEX_REGION_CLAUDE_4_0_SONNET"),
]


def get_vertex_region_for_model(model: str = None) -> str:
    """Get Vertex AI region for a specific model."""
    if model:
        for prefix, env_var in _VERTEX_REGION_OVERRIDES:
            if model.startswith(prefix):
                return os.environ.get(env_var) or get_default_vertex_region()
    return get_default_vertex_region()


__all__ = [
    "get_claude_config_home_dir",
    "get_teams_dir",
    "has_node_option",
    "is_env_truthy",
    "is_env_defined_falsy",
    "is_bare_mode",
    "parse_env_vars",
    "get_aws_region",
    "get_default_vertex_region",
    "should_maintain_project_working_dir",
    "is_running_on_homespace",
    "get_vertex_region_for_model",
]