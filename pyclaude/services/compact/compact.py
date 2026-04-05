"""
Compact service - conversation summarization.

This module provides functionality to compact conversation history
by summarizing older messages while preserving recent context.
"""

import os
from typing import Any, Dict, Optional
from dataclasses import dataclass


# Error messages
ERROR_MESSAGE_NOT_ENOUGH_MESSAGES = "Not enough messages to compact."
ERROR_MESSAGE_PROMPT_TOO_LONG = "Conversation too long. Press esc twice to go up a few messages and try again."
ERROR_MESSAGE_USER_ABORT = "API Error: Request was aborted."
ERROR_MESSAGE_INCOMPLETE_RESPONSE = "Compaction interrupted. This may be due to network issues — please try again."

# Constants
COMPACT_MAX_OUTPUT_TOKENS = 8192
POST_COMPACT_MAX_FILES_TO_RESTORE = 5
POST_COMPACT_TOKEN_BUDGET = 50_000
POST_COMPACT_MAX_TOKENS_PER_FILE = 5_000


@dataclass
class CompactionResult:
    """Result of a compaction operation."""
    boundary_marker: Dict[str, Any]
    summary_messages: list[Dict[str, Any]]
    attachments: list[Dict[str, Any]]
    hook_results: list[Dict[str, Any]]
    messages_to_keep: Optional[list[Dict[str, Any]]] = None
    user_display_message: Optional[str] = None
    pre_compact_token_count: Optional[int] = None
    post_compact_token_count: Optional[int] = None
    true_post_compact_token_count: Optional[int] = None
    compaction_usage: Optional[Dict[str, Any]] = None


def is_compact_disabled() -> bool:
    """Check if compact is disabled via environment variable."""
    return os.environ.get('DISABLE_COMPACT', '').lower() in ('1', 'true', 'yes')


def create_compact_boundary_message(
    trigger: str = "manual",
    pre_compact_token_count: int = 0,
    last_message_uuid: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a compact boundary marker message."""
    import uuid
    return {
        "type": "system",
        "role": "system",
        "content": f"[earlier conversation has been summarized - {pre_compact_token_count} tokens summarized]",
        "uuid": str(uuid.uuid4()),
        "isCompactBoundary": True,
        "compactMetadata": {
            "trigger": trigger,
            "preCompactTokenCount": pre_compact_token_count,
            "lastMessageUuid": last_message_uuid,
        },
    }


def get_compact_prompt(custom_instructions: Optional[str] = None) -> str:
    """Get the prompt for compact summarization."""
    base_prompt = """You are a helpful AI assistant. Your task is to summarize the conversation history in a concise way.

Provide a summary that:
1. Captures the main topics and goals discussed
2. Notes any important files or code that was worked on
3. Highlights any pending tasks or unresolved issues
4. Preserves context for continuing the conversation

Be concise but comprehensive - the summary should allow someone to understand what has been discussed without reading the full conversation."""

    if custom_instructions:
        base_prompt += f"\n\nAdditional instructions: {custom_instructions}"

    return base_prompt


def get_compact_user_summary_message(
    summary: str,
    suppress_follow_up_questions: bool = False,
    transcript_path: Optional[str] = None,
) -> str:
    """Create the summary message content."""
    content = f"## Conversation Summary\n\n{summary}"

    if suppress_follow_up_questions:
        content += "\n\n(Note: This summary was generated automatically.)"

    if transcript_path:
        content += f"\n\nFull transcript available at: {transcript_path}"

    return content


def estimate_tokens(text: str) -> int:
    """Rough estimate of token count (~4 chars per token)."""
    if not text:
        return 0
    return max(1, len(text) // 4)


def estimate_message_tokens(messages: list[Dict[str, Any]]) -> int:
    """Estimate tokens for a list of messages."""
    total = 0
    for msg in messages:
        content = msg.get('content', '')
        if isinstance(content, str):
            total += estimate_tokens(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    text = block.get('text', '')
                    if text:
                        total += estimate_tokens(text)
    return total


async def compact_conversation(
    messages: list[Dict[str, Any]],
    context: Dict[str, Any],
    cache_safe_params: Optional[Dict[str, Any]] = None,
    suppress_follow_up_questions: bool = False,
    custom_instructions: Optional[str] = None,
    is_auto_compact: bool = False,
) -> CompactionResult:
    """
    Create a compact version of a conversation by summarizing older messages.

    Args:
        messages: Current conversation messages
        context: Tool use context with get_app_state, set_app_state, etc.
        cache_safe_params: Cache sharing parameters
        suppress_follow_up_questions: Whether to suppress follow-up questions
        custom_instructions: Custom summarization instructions
        is_auto_compact: Whether this is an auto-compact

    Returns:
        CompactionResult with summary and boundary marker
    """
    if len(messages) == 0:
        raise ValueError(ERROR_MESSAGE_NOT_ENOUGH_MESSAGES)

    # Get app state
    get_app_state = context.get('get_app_state')
    set_app_state = context.get('set_app_state')
    read_file_state = context.get('read_file_state', {})

    app_state = get_app_state() if get_app_state else {}

    # Calculate pre-compact token count
    pre_compact_token_count = estimate_message_tokens(messages)

    # Build the compact request
    compact_prompt = get_compact_prompt(custom_instructions)

    # Create summary request message
    summary_request = {
        "type": "message",
        "role": "user",
        "content": [{"type": "text", "text": compact_prompt}],
    }

    # Filter messages to summarize (exclude recent ones)
    # Keep the last few messages as context
    keep_count = min(5, len(messages))
    messages_to_summarize = messages[:-keep_count] if keep_count > 0 else messages
    messages_to_keep = messages[-keep_count:] if keep_count > 0 else []

    if len(messages_to_summarize) == 0:
        raise ValueError(ERROR_MESSAGE_NOT_ENOUGH_MESSAGES)

    # Get model to use for summarization
    model = context.get('model', 'claude-sonnet-4-20250514')

    # Create a query to summarize the conversation
    # Use a simple approach: send the messages to summarize with the summary request
    from ...services.api import call_anthropic_api

    # Build messages for API call
    api_messages = []
    for msg in messages_to_summarize:
        if isinstance(msg, dict):
            api_messages.append(msg)

    # Add the summary request
    api_messages.append(summary_request)

    try:
        # Call the API to get the summary
        response = await call_anthropic_api(
            messages=api_messages,
            system_prompt="You are a helpful assistant tasked with summarizing conversations.",
            model=model,
            max_tokens=COMPACT_MAX_OUTPUT_TOKENS,
            thinking_config={"type": "disabled"},
        )

        # Extract summary from response
        summary = ""
        content = response.get('content', [])
        for block in content:
            if block.get('type') == 'text':
                summary = block.get('text', '')
                break

        if not summary:
            raise ValueError("Failed to generate summary - no text in response")

    except Exception as e:
        error_msg = str(e)
        if "aborted" in error_msg.lower():
            raise ValueError(ERROR_MESSAGE_USER_ABORT)
        elif "too long" in error_msg.lower() or "prompt" in error_msg.lower():
            raise ValueError(ERROR_MESSAGE_PROMPT_TOO_LONG)
        else:
            raise ValueError(f"Error during compaction: {error_msg}")

    # Get usage from response
    usage = response.get('usage', {})

    # Create boundary marker
    last_uuid = messages[-1].get('uuid') if messages else None
    boundary_marker = create_compact_boundary_message(
        trigger='auto' if is_auto_compact else 'manual',
        pre_compact_token_count=pre_compact_token_count,
        last_message_uuid=last_uuid,
    )

    # Create summary message
    summary_content = get_compact_user_summary_message(
        summary,
        suppress_follow_up_questions,
    )

    summary_message = {
        "type": "message",
        "role": "user",
        "content": [{"type": "text", "text": summary_content}],
        "isCompactSummary": True,
    }

    # Calculate post-compact token count
    post_compact_messages = [boundary_marker, summary_message] + messages_to_keep
    post_compact_token_count = estimate_message_tokens(post_compact_messages)

    # Clear read file state after compaction
    if read_file_state and hasattr(read_file_state, 'clear'):
        read_file_state.clear()

    return CompactionResult(
        boundary_marker=boundary_marker,
        summary_messages=[summary_message],
        attachments=[],
        hook_results=[],
        messages_to_keep=messages_to_keep,
        user_display_message=None,
        pre_compact_token_count=pre_compact_token_count,
        post_compact_token_count=post_compact_token_count,
        true_post_compact_token_count=post_compact_token_count,
        compaction_usage=usage,
    )


def build_post_compact_messages(result: CompactionResult) -> list[Dict[str, Any]]:
    """Build the messages array after compaction."""
    messages = [
        result.boundary_marker,
        *result.summary_messages,
    ]

    if result.messages_to_keep:
        messages.extend(result.messages_to_keep)

    messages.extend(result.attachments)
    messages.extend(result.hook_results)

    return messages


def create_compact_can_use_tool():
    """Create a tool permission function that denies all tools during compaction."""
    async def deny_tools(
        tool_name: str,
        input_dict: Dict[str, Any],
        tool_use_context: Any,
        assistant_message: Any,
        tool_use_id: str,
    ) -> Dict[str, Any]:
        return {
            "behavior": "deny",
            "message": "Tool use is not allowed during compaction",
            "decisionReason": {
                "type": "other",
                "reason": "compaction agent should only produce text summary",
            },
        }

    return deny_tools


__all__ = [
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
]