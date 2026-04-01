"""
Thinking configuration utilities.
"""

import os
from typing import Any, Optional


class ThinkingConfig:
    """Thinking configuration for Claude."""

    def __init__(
        self,
        type: str = 'adaptive',  # 'adaptive', 'enabled', 'disabled'
        budget_tokens: Optional[int] = None,
    ):
        self.type = type
        self.budget_tokens = budget_tokens

    def to_dict(self) -> dict:
        result = {'type': self.type}
        if self.budget_tokens:
            result['budget_tokens'] = self.budget_tokens
        return result


def should_enable_thinking_by_default() -> Optional[bool]:
    """Check if thinking should be enabled by default."""
    env = os.environ.get('CLAUDE_THINKING')
    if env == 'true':
        return True
    if env == 'false':
        return False
    return None  # Use default behavior


def get_thinking_config() -> ThinkingConfig:
    """Get thinking configuration."""
    env = os.environ.get('CLAUDE_THINKING')

    if env == 'false':
        return ThinkingConfig(type='disabled')
    if env == 'true':
        return ThinkingConfig(type='enabled')

    # Default: adaptive
    return ThinkingConfig(type='adaptive')


__all__ = ['ThinkingConfig', 'should_enable_thinking_by_default', 'get_thinking_config']