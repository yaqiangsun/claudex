"""
Compact service - conversation summarization.

This module provides functionality to compact conversation history
by summarizing older messages while preserving recent context.
"""

from .compact import (
    CompactionResult,
    compact_conversation,
    build_post_compact_messages,
    create_compact_can_use_tool,
    create_compact_boundary_message,
    get_compact_prompt,
    get_compact_user_summary_message,
    estimate_tokens,
    estimate_message_tokens,
    is_compact_disabled,
    ERROR_MESSAGE_NOT_ENOUGH_MESSAGES,
    ERROR_MESSAGE_PROMPT_TOO_LONG,
    ERROR_MESSAGE_USER_ABORT,
    ERROR_MESSAGE_INCOMPLETE_RESPONSE,
)

from .autoCompact import (
    AutoCompactTrackingState,
    auto_compact_if_needed,
    should_auto_compact,
    is_auto_compact_enabled,
    get_auto_compact_threshold,
    get_effective_context_window_size,
    calculate_token_warning_state,
    create_auto_compact_tracking,
    AUTOCOMPACT_BUFFER_TOKENS,
    WARNING_THRESHOLD_BUFFER_TOKENS,
    ERROR_THRESHOLD_BUFFER_TOKENS,
    MANUAL_COMPACT_BUFFER_TOKENS,
    MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES,
)

__all__ = [
    # Compact
    "CompactionResult",
    "compact_conversation",
    "build_post_compact_messages",
    "create_compact_can_use_tool",
    "create_compact_boundary_message",
    "get_compact_prompt",
    "get_compact_user_summary_message",
    "estimate_tokens",
    "estimate_message_tokens",
    "ERROR_MESSAGE_NOT_ENOUGH_MESSAGES",
    "ERROR_MESSAGE_PROMPT_TOO_LONG",
    "ERROR_MESSAGE_USER_ABORT",
    "ERROR_MESSAGE_INCOMPLETE_RESPONSE",
    # Auto-compact
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