"""
Truncation utilities - width-aware string truncation.

Python adaptation.
"""

import re
from typing import List


def string_width(s: str) -> int:
    """Get the display width of a string (considering CJK, emoji, etc).

    Simplified implementation - counts most characters as 1,
    full-width characters as 2.
    """
    width = 0
    for char in s:
        # Full-width characters (CJK, etc)
        if ord(char) >= 0x1100 and (
            (0x1100 <= ord(char) <= 0x115F) or  # Hangul Jamo
            (0x2329 <= ord(char) <= 0x232A) or  # Angled brackets
            (0x2E80 <= ord(char) <= 0x303E) or  # CJK
            (0x3040 <= ord(char) <= 0xA4CF) or
            (0xAC00 <= ord(char) <= 0xD7A3) or  # Hangul
            (0xF900 <= ord(char) <= 0xFAFF) or  # CJK compatibility
            (0xFE10 <= ord(char) <= 0xFE19) or  # Vertical forms
            (0xFE30 <= ord(char) <= 0xFE6F) or  # CJK compatibility forms
            (0xFF00 <= ord(char) <= 0xFF60) or  # Fullwidth forms
            (0xFFE0 <= ord(char) <= 0xFFE6) or
            (0x20000 <= ord(char) <= 0x2FFFD) or
            (0x30000 <= ord(char) <= 0x3FFFD)
        ):
            width += 2
        else:
            width += 1
    return width


def truncate_path_middle(path: str, max_length: int) -> str:
    """Truncates a file path in the middle to preserve both directory context and filename.

    Width-aware: uses stringWidth() for correct CJK/emoji measurement.
    For example: "src/components/deeply/nested/folder/MyComponent.tsx" becomes
    "src/components/…/MyComponent.tsx" when maxLength is 30.

    Args:
        path: The file path to truncate
        max_length: Maximum display width of the result in terminal columns

    Returns:
        The truncated path, or original if it fits within max_length
    """
    # No truncation needed
    if string_width(path) <= max_length:
        return path

    # Handle edge case
    if max_length <= 0:
        return "…"

    # Need at least room for "…" + something meaningful
    if max_length < 5:
        return truncate_to_width(path, max_length)

    # Find the filename (last path segment)
    last_slash = path.rfind("/")
    filename = path[last_slash:] if last_slash >= 0 else path
    directory = path[:last_slash] if last_slash >= 0 else ""
    filename_width = string_width(filename)

    # If filename alone is too long, truncate from start
    if filename_width >= max_length - 1:
        return truncate_start_to_width(path, max_length)

    # Calculate space available for directory prefix
    available_for_dir = max_length - 1 - filename_width  # -1 for ellipsis

    if available_for_dir <= 0:
        return truncate_start_to_width(filename, max_length)

    # Truncate directory and combine
    truncated_dir = truncate_to_width_no_ellipsis(directory, available_for_dir)
    return truncated_dir + "…" + filename


def truncate_to_width(text: str, max_width: int) -> str:
    """Truncates a string to fit within a maximum display width.

    Appends '…' when truncation occurs.
    """
    if string_width(text) <= max_width:
        return text
    if max_width <= 1:
        return "…"

    width = 0
    result = ""
    for char in text:
        char_width = string_width(char)
        if width + char_width > max_width - 1:
            break
        result += char
        width += char_width
    return result + "…"


def truncate_start_to_width(text: str, max_width: int) -> str:
    """Truncates from the start of a string, keeping the tail end.

    Prepends '…' when truncation occurs.
    """
    if string_width(text) <= max_width:
        return text
    if max_width <= 1:
        return "…"

    # Work backwards from the end
    chars = list(text)
    width = 0
    start_idx = len(chars)

    for i in range(len(chars) - 1, -1, -1):
        char_width = string_width(chars[i])
        if width + char_width > max_width - 1:  # -1 for '…'
            break
        width += char_width
        start_idx = i

    return "…" + "".join(chars[start_idx:])


def truncate_to_width_no_ellipsis(text: str, max_width: int) -> str:
    """Truncates a string without appending an ellipsis."""
    if string_width(text) <= max_width:
        return text
    if max_width <= 0:
        return ""

    width = 0
    result = ""
    for char in text:
        char_width = string_width(char)
        if width + char_width > max_width:
            break
        result += char
        width += char_width
    return result


def truncate(text: str, max_width: int, single_line: bool = False) -> str:
    """Truncates a string to fit within a maximum display width.

    Args:
        text: The string to truncate
        max_width: Maximum display width in terminal columns
        single_line: If true, also truncates at the first newline

    Returns:
        The truncated string with ellipsis if needed
    """
    result = text

    # If single_line is true, truncate at first newline
    if single_line:
        first_newline = text.find("\n")
        if first_newline != -1:
            result = text[:first_newline]
            if string_width(result) + 1 > max_width:
                return truncate_to_width(result, max_width)
            return f"{result}…"

    if string_width(result) <= max_width:
        return result
    return truncate_to_width(result, max_width)


def wrap_text(text: str, width: int) -> List[str]:
    """Wrap text to specified width."""
    lines: List[str] = []
    current_line = ""
    current_width = 0

    for char in text:
        char_width = string_width(char)
        if current_width + char_width <= width:
            current_line += char
            current_width += char_width
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
            current_width = char_width

    if current_line:
        lines.append(current_line)
    return lines


__all__ = [
    "string_width",
    "truncate_path_middle",
    "truncate_to_width",
    "truncate_start_to_width",
    "truncate_to_width_no_ellipsis",
    "truncate",
    "wrap_text",
]