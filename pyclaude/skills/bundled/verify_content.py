"""Verify Content - SKILL_FILES for verify skill.

This module provides reference content for the verify skill.
In the original TS, these are loaded from .md files at build time.
"""
from __future__ import annotations


# Reference files available for the verify skill
# These would be populated from .md files in a full implementation
SKILL_FILES: dict[str, str] = {
    # Note: In the original TS, these are loaded from ./verify/*.md files
    # When actual examples are added, populate this dict with file contents.
    # 'examples/cli.md': ...,
    # 'examples/server.md': ...,
}


__all__ = ['SKILL_FILES']