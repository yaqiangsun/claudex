"""
Managed env constants utilities.

Managed environment constants.
"""

# Managed environment variable names
MANAGED_ENV_VARS = [
    "CLAUDE_CODE",
    "CLAUDE_CODE_SESSION_ID",
    "CLAUDE_CODE_CWD",
]

# Environment variable prefixes
ENV_PREFIX = "CLAUDE_CODE_"


def is_managed_env_var(name: str) -> bool:
    """Check if env var is managed."""
    return name in MANAGED_ENV_VARS or name.startswith(ENV_PREFIX)


__all__ = [
    "MANAGED_ENV_VARS",
    "ENV_PREFIX",
    "is_managed_env_var",
]