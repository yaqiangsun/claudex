"""Common constants and utilities."""

import os
from functools import lru_cache


def get_local_iso_date() -> str:
    """Get the local date in ISO format (YYYY-MM-DD)."""
    # Check for ant-only date override
    override = os.environ.get('CLAUDE_CODE_OVERRIDE_DATE')
    if override:
        return override

    now = __import__('datetime').datetime.now()
    year = now.year
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    return f"{year}-{month}-{day}"


# Memoized for prompt-cache stability — captures the date once at session start.
# The main interactive path gets this behavior via memoize(getUserContext) in
# context.ts; simple mode (--bare) calls getSystemPrompt per-request and needs
# an explicit memoized date to avoid busting the cached prefix at midnight.
# When midnight rolls over, getDateChangeAttachments appends the new date at
# the tail (though simple mode disables attachments, so the trade-off there is:
# stale date after midnight vs. ~entire-conversation cache bust — stale wins).
get_session_start_date = lru_cache(maxsize=1)(get_local_iso_date)


def get_local_month_year() -> str:
    """Returns 'Month YYYY' (e.g. 'February 2026') in the user's local timezone."""
    override = os.environ.get('CLAUDE_CODE_OVERRIDE_DATE')
    if override:
        date = __import__('datetime').datetime.fromisoformat(override)
    else:
        date = __import__('datetime').datetime.now()

    return date.strftime('%B %Y')