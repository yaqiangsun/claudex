"""
Hook to run code after first render.

Python adaptation - called after the TUI has been rendered for the first time.
"""

import os
import time


_first_render_done = False
_start_time = time.time()


def after_first_render() -> bool:
    """Check if this is the first render and run startup code if needed."""
    global _first_render_done, _start_time

    if _first_render_done:
        return False

    _first_render_done = True

    # Run startup code for ants
    if os.environ.get("USER_TYPE") == "ant" and os.environ.get("CLAUDE_CODE_EXIT_AFTER_FIRST_RENDER"):
        elapsed_ms = round((time.time() - _start_time) * 1000)
        print(f"\nStartup time: {elapsed_ms}ms")
        return True

    return False


__all__ = ["after_first_render", "_first_render_done"]