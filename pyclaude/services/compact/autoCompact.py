"""
Auto-compact service - automatic conversation summarization.

This module provides functionality to automatically compact conversations
when they approach the context window limit.
"""

import os
from typing import Any, Dict, Optional
from dataclasses import dataclass, field

from .compact import (
    CompactionResult,
    compact_conversation,
    estimate_message_tokens,
    ERROR_MESSAGE_USER_ABORT,
)


# Token reserves for output during compaction
MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000

# Buffer tokens
AUTOCOMPACT_BUFFER_TOKENS = 13_000
WARNING_THRESHOLD_BUFFER_TOKENS = 20_000
ERROR_THRESHOLD_BUFFER_TOKENS = 20_000
MANUAL_COMPACT_BUFFER_TOKENS = 3_000

# Circuit breaker for consecutive failures
MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3


@dataclass
class AutoCompactTrackingState:
    """Tracks auto-compact state across turns."""
    compacted: bool = False
    turn_counter: int = 0
    turn_id: str = ""
    consecutive_failures: int = 0


def get_context_window_for_model(model: str) -> int:
    """Get the context window size for a model."""
    # Default context windows for common models
    model_windows = {
        "claude-opus-4-5-20250514": 200000,
        "claude-sonnet-4-20250514": 200000,
        "claude-haiku-4-20250514": 200000,
        "MiniMaxAI/MiniMax-M2.5": 100000,
        "MiniMaxAI/MiniMax-M2.8": 100000,
    }
    return model_windows.get(model, 100000)


def get_effective_context_window_size(model: str) -> int:
    """Get effective context window (minus reserved output tokens)."""
    reserved_tokens = min(MAX_OUTPUT_TOKENS_FOR_SUMMARY, 8192)
    context_window = get_context_window_for_model(model)

    # Allow environment override
    auto_compact_window = os.environ.get("CLAUDE_CODE_AUTO_COMPACT_WINDOW")
    if auto_compact_window:
        try:
            parsed = int(auto_compact_window)
            if parsed > 0:
                context_window = min(context_window, parsed)
        except ValueError:
            pass

    return context_window - reserved_tokens


def get_auto_compact_threshold(model: str) -> int:
    """Get the token threshold for triggering auto-compact."""
    effective_context_window = get_effective_context_window_size(model)
    threshold = effective_context_window - AUTOCOMPACT_BUFFER_TOKENS

    # Allow percentage override for testing
    env_percent = os.environ.get("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE")
    if env_percent:
        try:
            parsed = float(env_percent)
            if parsed > 0 and parsed <= 100:
                percentage_threshold = int(effective_context_window * (parsed / 100))
                return min(percentage_threshold, threshold)
        except ValueError:
            pass

    return threshold


def calculate_token_warning_state(
    token_usage: int,
    model: str,
) -> Dict[str, Any]:
    """Calculate token warning state for UI display."""
    auto_compact_threshold = get_auto_compact_threshold(model)
    effective_window = get_effective_context_window_size(model)

    # Use auto-compact threshold if enabled, otherwise use effective window
    if is_auto_compact_enabled():
        threshold = auto_compact_threshold
    else:
        threshold = effective_window

    if threshold > 0:
        percent_left = max(0, round(((threshold - token_usage) / threshold) * 100))
    else:
        percent_left = 0

    warning_threshold = threshold - WARNING_THRESHOLD_BUFFER_TOKENS
    error_threshold = threshold - ERROR_THRESHOLD_BUFFER_TOKENS

    is_above_warning = token_usage >= warning_threshold
    is_above_error = token_usage >= error_threshold
    is_above_auto_compact = is_auto_compact_enabled() and token_usage >= auto_compact_threshold

    # Calculate blocking limit
    default_blocking = effective_window - MANUAL_COMPACT_BUFFER_TOKENS
    blocking_override = os.environ.get("CLAUDE_CODE_BLOCKING_LIMIT_OVERRIDE")
    try:
        blocking_limit = int(blocking_override) if blocking_override else default_blocking
    except ValueError:
        blocking_limit = default_blocking

    is_at_blocking = token_usage >= blocking_limit

    return {
        "percentLeft": percent_left,
        "isAboveWarningThreshold": is_above_warning,
        "isAboveErrorThreshold": is_above_error,
        "isAboveAutoCompactThreshold": is_above_auto_compact,
        "isAtBlockingLimit": is_at_blocking,
    }


def is_auto_compact_enabled() -> bool:
    """Check if auto-compact is enabled."""
    # Check environment variables
    if os.environ.get("DISABLE_COMPACT", "").lower() in ("1", "true", "yes"):
        return False
    if os.environ.get("DISABLE_AUTO_COMPACT", "").lower() in ("1", "true", "yes"):
        return False

    # Check user config (if available)
    try:
        from ...utils.config import get_global_config
        config = get_global_config()
        if hasattr(config, "auto_compact_enabled"):
            return config.auto_compact_enabled
    except Exception:
        pass

    # Default to enabled
    return True


async def should_auto_compact(
    messages: list[Dict[str, Any]],
    model: str,
    query_source: Optional[str] = None,
    snip_tokens_freed: int = 0,
) -> bool:
    """Determine if auto-compact should be triggered."""
    # Don't compact in nested queries (session_memory, compact)
    if query_source in ("session_memory", "compact"):
        return False

    if not is_auto_compact_enabled():
        return False

    # Calculate token count
    token_count = estimate_message_tokens(messages) - snip_tokens_freed
    threshold = get_auto_compact_threshold(model)

    # Log for debugging
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"autocompact: tokens={token_count} threshold={threshold}")

    return token_count >= threshold


async def auto_compact_if_needed(
    messages: list[Dict[str, Any]],
    tool_use_context: Dict[str, Any],
    cache_safe_params: Optional[Dict[str, Any]] = None,
    query_source: Optional[str] = None,
    tracking: Optional[AutoCompactTrackingState] = None,
    snip_tokens_freed: int = 0,
) -> Dict[str, Any]:
    """
    Automatically compact the conversation if needed.

    Args:
        messages: Current conversation messages
        tool_use_context: Context with get_app_state, set_app_state, etc.
        cache_safe_params: Cache sharing parameters
        query_source: Source of the query (e.g., 'compact', 'session_memory')
        tracking: Tracking state from previous turns
        snip_tokens_freed: Tokens freed by snip operation

    Returns:
        Dict with was_compacted, compaction_result, and consecutive_failures
    """
    # Check if compact is disabled
    if os.environ.get("DISABLE_COMPACT", "").lower() in ("1", "true", "yes"):
        return {"was_compacted": False}

    # Circuit breaker: stop after too many consecutive failures
    if tracking and tracking.consecutive_failures >= MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES:
        return {"was_compacted": False}

    model = tool_use_context.get("model", "claude-sonnet-4-20250514")

    # Check if we should auto-compact
    should_compact = await should_auto_compact(
        messages,
        model,
        query_source,
        snip_tokens_freed,
    )

    if not should_compact:
        return {"was_compacted": False}

    try:
        # Perform the compaction
        compaction_result = await compact_conversation(
            messages=messages,
            context=tool_use_context,
            cache_safe_params=cache_safe_params,
            suppress_follow_up_questions=True,  # Auto-compact suppresses follow-ups
            custom_instructions=None,
            is_auto_compact=True,
        )

        # Return success
        return {
            "was_compacted": True,
            "compaction_result": compaction_result,
            "consecutive_failures": 0,
        }

    except Exception as e:
        error_msg = str(e).lower()

        # Only log non-abort errors
        if "abort" not in error_msg:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Auto-compact error: {e}")

        # Increment failure count for circuit breaker
        prev_failures = tracking.consecutive_failures if tracking else 0
        next_failures = prev_failures + 1

        return {
            "was_compacted": False,
            "consecutive_failures": next_failures,
        }


def create_auto_compact_tracking() -> AutoCompactTrackingState:
    """Create a new auto-compact tracking state."""
    import uuid
    return AutoCompactTrackingState(
        compacted=False,
        turn_counter=0,
        turn_id=str(uuid.uuid4()),
        consecutive_failures=0,
    )


__all__ = [
    "AutoCompactTrackingState",
    "auto_compact_if_needed",
    "should_auto_compact",
    "is_auto_compact_enabled",
    "get_auto_compact_threshold",
    "get_effective_context_window_size",
    "calculate_token_warning_state",
    "create_auto_compact_tracking",
    "AUTOCOMPACT_BUFFER_TOKENS",
    "WARNING_THRESHOLD_BUFFER_TOKENS",
    "ERROR_THRESHOLD_BUFFER_TOKENS",
    "MANUAL_COMPACT_BUFFER_TOKENS",
    "MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES",
]