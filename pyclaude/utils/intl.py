"""
Internationalization utilities - Intl object equivalents.

Python adaptation using built-in libraries.
"""

import os
from typing import Optional
from functools import lru_cache


# Grapheme segmenter - simplified implementation
@lru_cache(maxsize=1)
def get_grapheme_segmenter():
    """Get grapheme segmenter (cached)."""
    # In Python, we'll use a simple list-based approach
    return GraphemeSegmenter()


class GraphemeSegmenter:
    """Simple grapheme segmenter for Python."""

    def segment(self, text: str):
        """Segment text into graphemes."""
        if not text:
            return []
        # Simple approach: treat each character as a grapheme
        # A proper implementation would handle emoji, combining chars, etc.
        return [GraphemeSegment(text[i], i) for i in range(len(text))]


class GraphemeSegment:
    """A segment of text."""

    def __init__(self, segment: str, index: int):
        self.segment = segment
        self._index = index


def first_grapheme(text: str) -> str:
    """Extract the first grapheme cluster from a string."""
    if not text:
        return ""
    return text[0]


def last_grapheme(text: str) -> str:
    """Extract the last grapheme cluster from a string."""
    if not text:
        return ""
    return text[-1]


# Word segmenter
@lru_cache(maxsize=1)
def get_word_segmenter():
    """Get word segmenter (cached)."""
    return WordSegmenter()


class WordSegmenter:
    """Simple word segmenter for Python."""

    def segment(self, text: str):
        """Segment text into words."""
        if not text:
            return []
        import re
        # Split on whitespace and punctuation
        words = re.findall(r'\S+', text)
        return [WordSegment(w, i) for i, w in enumerate(words)]


class WordSegment:
    """A word segment."""

    def __init__(self, segment: str, index: int):
        self.segment = segment
        self._index = index


# RelativeTimeFormat - simplified
class RelativeTimeFormat:
    """Relative time format equivalent."""

    def __init__(self, locale: str, style: str = "long", numeric: str = "always"):
        self.locale = locale
        self.style = style
        self.numeric = numeric

    def format(self, value: int, unit: str) -> str:
        """Format relative time."""
        if self.numeric == "always":
            if value == 1:
                return f"1 {unit}"
            return f"{value} {unit}s"
        # For 'auto', we'd need more complex logic
        return f"{value} {unit}"


# Cache for RelativeTimeFormat instances
_rtf_cache = {}


def get_relative_time_format(
    style: str = "long",
    numeric: str = "always",
) -> RelativeTimeFormat:
    """Get a RelativeTimeFormat instance."""
    key = f"{style}:{numeric}"
    if key not in _rtf_cache:
        _rtf_cache[key] = RelativeTimeFormat("en", style, numeric)
    return _rtf_cache[key]


# Timezone cache
_cached_time_zone: Optional[str] = None


def get_time_zone() -> str:
    """Get the current timezone."""
    global _cached_time_zone
    if _cached_time_zone is None:
        try:
            import time
            _cached_time_zone = time.tzname[0] or "UTC"
        except Exception:
            _cached_time_zone = "UTC"
    return _cached_time_zone


# System locale language cache
_cached_system_locale_language: Optional[str] = None


def get_system_locale_language() -> Optional[str]:
    """Get the system locale language (e.g., 'en', 'ja')."""
    global _cached_system_locale_language

    if _cached_system_locale_language is None:
        try:
            import locale
            loc = locale.getdefaultlocale()
            if loc and loc[0]:
                _cached_system_locale_language = loc[0].split("_")[0]
            else:
                _cached_system_locale_language = None
        except Exception:
            _cached_system_locale_language = None

    return _cached_system_locale_language


__all__ = [
    "get_grapheme_segmenter",
    "first_grapheme",
    "last_grapheme",
    "get_word_segmenter",
    "get_relative_time_format",
    "get_time_zone",
    "get_system_locale_language",
    "RelativeTimeFormat",
]