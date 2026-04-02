"""
Context window and model token utilities.

Python adaptation.
"""

import os
import re
from typing import Dict, Optional, Tuple


# Model context window size (200k tokens for all models right now)
MODEL_CONTEXT_WINDOW_DEFAULT = 200_000

# Maximum output tokens for compact operations
COMPACT_MAX_OUTPUT_TOKENS = 20_000

# Default max output tokens
MAX_OUTPUT_TOKENS_DEFAULT = 32_000
MAX_OUTPUT_TOKENS_UPPER_LIMIT = 64_000

# Capped default for slot-reservation optimization
CAPPED_DEFAULT_MAX_TOKENS = 8_000
ESCALATED_MAX_TOKENS = 64_000


def is_1m_context_disabled() -> bool:
    """Check if 1M context is disabled via environment variable."""
    env_val = os.environ.get("CLAUDE_CODE_DISABLE_1M_CONTEXT")
    if env_val:
        return env_val.lower() in ("1", "true", "yes", "on")
    return False


def has_1m_context(model: str) -> bool:
    """Check if model has 1M context based on name."""
    if is_1m_context_disabled():
        return False
    return bool(re.search(r"\[1m\]", model, re.IGNORECASE))


def model_supports_1m(model: str) -> bool:
    """Check if model supports 1M context."""
    if is_1m_context_disabled():
        return False
    model_lower = model.lower()
    return "claude-sonnet-4" in model_lower or "opus-4-6" in model_lower


def get_context_window_for_model(model: str, betas: Optional[list] = None) -> int:
    """Get context window size for a model."""
    # Allow override via environment variable (ant-only)
    if os.environ.get("USER_TYPE") == "ant":
        override_str = os.environ.get("CLAUDE_CODE_MAX_CONTEXT_TOKENS")
        if override_str:
            try:
                override = int(override_str)
                if override > 0:
                    return override
            except ValueError:
                pass

    # [1m] suffix — explicit client-side opt-in
    if has_1m_context(model):
        return 1_000_000

    # Default to 200k
    return MODEL_CONTEXT_WINDOW_DEFAULT


def get_model_max_output_tokens(model: str) -> Dict[str, int]:
    """Get model's default and upper limit for max output tokens."""
    model_lower = model.lower()

    if "opus-4-6" in model_lower:
        default_tokens = 64_000
        upper_limit = 128_000
    elif "sonnet-4-6" in model_lower:
        default_tokens = 32_000
        upper_limit = 128_000
    elif "opus-4-5" in model_lower or "sonnet-4" in model_lower or "haiku-4" in model_lower:
        default_tokens = 32_000
        upper_limit = 64_000
    elif "opus-4-1" in model_lower or "opus-4" in model_lower:
        default_tokens = 32_000
        upper_limit = 32_000
    elif "claude-3-opus" in model_lower:
        default_tokens = 4_096
        upper_limit = 4_096
    elif "claude-3-sonnet" in model_lower:
        default_tokens = 8_192
        upper_limit = 8_192
    elif "claude-3-haiku" in model_lower:
        default_tokens = 4_096
        upper_limit = 4_096
    elif "3-5-sonnet" in model_lower or "3-5-haiku" in model_lower:
        default_tokens = 8_192
        upper_limit = 8_192
    elif "3-7-sonnet" in model_lower:
        default_tokens = 32_000
        upper_limit = 64_000
    else:
        default_tokens = MAX_OUTPUT_TOKENS_DEFAULT
        upper_limit = MAX_OUTPUT_TOKENS_UPPER_LIMIT

    return {"default": default_tokens, "upperLimit": upper_limit}


def get_max_thinking_tokens_for_model(model: str) -> int:
    """Get max thinking budget tokens for a model."""
    return get_model_max_output_tokens(model)["upperLimit"] - 1


def calculate_context_percentages(
    current_usage: Optional[Dict[str, int]],
    context_window_size: int,
) -> Dict[str, Optional[float]]:
    """Calculate context window usage percentage."""
    if not current_usage:
        return {"used": None, "remaining": None}

    total_input_tokens = (
        current_usage.get("input_tokens", 0) +
        current_usage.get("cache_creation_input_tokens", 0) +
        current_usage.get("cache_read_input_tokens", 0)
    )

    used_percentage = round((total_input_tokens / context_window_size) * 100)
    clamped_used = min(100, max(0, used_percentage))

    return {
        "used": clamped_used,
        "remaining": 100 - clamped_used,
    }


__all__ = [
    "MODEL_CONTEXT_WINDOW_DEFAULT",
    "COMPACT_MAX_OUTPUT_TOKENS",
    "CAPPED_DEFAULT_MAX_TOKENS",
    "ESCALATED_MAX_TOKENS",
    "is_1m_context_disabled",
    "has_1m_context",
    "model_supports_1m",
    "get_context_window_for_model",
    "get_model_max_output_tokens",
    "get_max_thinking_tokens_for_model",
    "calculate_context_percentages",
]