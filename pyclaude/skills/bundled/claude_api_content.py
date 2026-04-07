"""Claude API Content - SKILL_FILES for claude-api skill.

This module provides reference content for the claude-api skill.
In the original TS, these are loaded from .md files at build time.

Since the .md files are not present, this provides a placeholder structure
that can be extended when the documentation files are available.
"""
from __future__ import annotations


# Model IDs/names for variable substitution in prompts
SKILL_MODEL_VARS = {
    'OPUS_ID': 'claude-opus-4-6',
    'OPUS_NAME': 'Claude Opus 4.6',
    'SONNET_ID': 'claude-sonnet-4-6',
    'SONNET_NAME': 'Claude Sonnet 4.6',
    'HAIKU_ID': 'claude-haiku-4-5',
    'HAIKU_NAME': 'Claude Haiku 4.5',
    'PREV_SONNET_ID': 'claude-sonnet-4-5',
}


# Reference files available for the claude-api skill
# These would be populated from .md files in a full implementation
SKILL_FILES: dict[str, str] = {
    # Note: In the original TS, these are loaded from ./claude-api/*.md files
    # at build time via Bun's text loader. For now, this is a placeholder.
    # When actual docs are added, populate this dict with file contents.
}


__all__ = ['SKILL_MODEL_VARS', 'SKILL_FILES']