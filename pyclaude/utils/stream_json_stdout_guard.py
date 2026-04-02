"""
Stream JSON stdout guard utilities.

Guard JSON output to stdout.
"""

import json
import sys
from typing import Any


def write_json_to_stdout(data: Any) -> None:
    """Write JSON to stdout safely."""
    try:
        sys.stdout.write(json.dumps(data))
        sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception:
        pass


__all__ = ["write_json_to_stdout"]