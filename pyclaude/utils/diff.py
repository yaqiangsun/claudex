"""
Diff utilities.

Python adaptation using difflib.
"""

import difflib
from typing import List, Dict, Any, Optional


# Constants
CONTEXT_LINES = 3
DIFF_TIMEOUT_MS = 5000

# Token replacement for diff library
_AMPERSAND_TOKEN = "<<:AMPERSAND_TOKEN:>>"
_DOLLAR_TOKEN = "<<:DOLLAR_TOKEN:>>"


def _escape_for_diff(s: str) -> str:
    """Escape special characters for diff."""
    return s.replace("&", _AMPERSAND_TOKEN).replace("$", _DOLLAR_TOKEN)


def _unescape_from_diff(s: str) -> str:
    """Unescape special characters after diff."""
    return s.replace(_AMPERSAND_TOKEN, "&").replace(_DOLLAR_TOKEN, "$")


def adjust_hunk_line_numbers(
    hunks: List[Dict[str, Any]],
    offset: int,
) -> List[Dict[str, Any]]:
    """Shift hunk line numbers by offset."""
    if offset == 0:
        return hunks
    return [
        {
            **h,
            "oldStart": h.get("oldStart", 0) + offset,
            "newStart": h.get("newStart", 0) + offset,
        }
        for h in hunks
    ]


def count_lines_changed(
    patch: List[Dict[str, Any]],
    new_file_content: Optional[str] = None,
) -> Dict[str, int]:
    """Count lines added and removed in a patch."""
    num_additions = 0
    num_removals = 0

    if len(patch) == 0 and new_file_content:
        # For new files, count all lines as additions
        num_additions = len(new_file_content.splitlines())
    else:
        for hunk in patch:
            lines = hunk.get("lines", [])
            num_additions += sum(1 for line in lines if line.startswith("+"))
            num_removals += sum(1 for line in lines if line.startswith("-"))

    return {"added": num_additions, "removed": num_removals}


def get_patch_from_contents(
    file_path: str,
    old_content: str,
    new_content: str,
    ignore_whitespace: bool = False,
    single_hunk: bool = False,
) -> List[Dict[str, Any]]:
    """Get unified diff patch from old and new content."""
    old_escaped = _escape_for_diff(old_content)
    new_escaped = _escape_for_diff(new_content)

    # Use difflib to generate unified diff
    from_lines = old_escaped.splitlines(keepends=True)
    to_lines = new_escaped.splitlines(keepends=True)

    # Generate unified diff
    diff = list(
        difflib.unified_diff(
            from_lines,
            to_lines,
            fromfile=file_path,
            tofile=file_path,
            lineterm="",
            n=CONTEXT_LINES if not single_hunk else 100000,
        )
    )

    if not diff:
        return []

    # Parse the diff output into hunks
    hunks = _parse_unified_diff(diff)
    return hunks


def _parse_unified_diff(diff_lines: List[str]) -> List[Dict[str, Any]]:
    """Parse unified diff output into hunk structures."""
    hunks = []
    current_hunk = None
    old_start = 0
    old_count = 0
    new_start = 0
    new_count = 0

    for line in diff_lines:
        if line.startswith("@@"):
            # Save previous hunk
            if current_hunk:
                hunks.append(current_hunk)

            # Parse new hunk header
            # @@ -old_start,old_count +new_start,new_count @@
            import re

            match = re.match(r"@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@", line)
            if match:
                old_start = int(match.group(1))
                old_count = int(match.group(2)) if match.group(2) else 1
                new_start = int(match.group(3))
                new_count = int(match.group(4)) if match.group(4) else 1

                current_hunk = {
                    "oldStart": old_start,
                    "oldLines": old_count,
                    "newStart": new_start,
                    "newLines": new_count,
                    "lines": [],
                }
        elif current_hunk is not None and line.startswith(("+", "-", " ")):
            current_hunk["lines"].append(_unescape_from_diff(line.rstrip("\n")))

    # Save last hunk
    if current_hunk:
        hunks.append(current_hunk)

    return hunks


def get_patch_for_display(
    file_path: str,
    file_contents: str,
    edits: List[Dict[str, Any]],
    ignore_whitespace: bool = False,
) -> List[Dict[str, Any]]:
    """Get patch for display with edits applied."""
    # Convert tabs to spaces
    prepared_contents = file_contents.expandtabs()

    # Apply edits
    new_content = prepared_contents
    for edit in edits:
        old_string = edit.get("old_string", "")
        new_string = edit.get("new_string", "")
        replace_all = edit.get("replace_all", False)

        # Convert tabs
        old_string = old_string.expandtabs()
        new_string = new_string.expandtabs()

        old_escaped = _escape_for_diff(old_string)
        new_escaped = _escape_for_diff(new_string)

        if replace_all:
            new_content = new_content.replace(old_escaped, new_escaped)
        else:
            new_content = new_content.replace(old_escaped, new_escaped, 1)

    # Generate diff
    return get_patch_from_contents(
        file_path,
        prepared_contents,
        new_content,
        ignore_whitespace=ignore_whitespace,
    )


__all__ = [
    "CONTEXT_LINES",
    "DIFF_TIMEOUT_MS",
    "adjust_hunk_line_numbers",
    "count_lines_changed",
    "get_patch_from_contents",
    "get_patch_for_display",
]