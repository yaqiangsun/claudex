"""
Exec file no throw utilities.

Execute file without throwing exceptions.
"""

import subprocess
from typing import Optional, Dict, Any


def exec_file_no_throw(
    command: str,
    args: list = None,
    options: Optional[Dict[str, Any]] = None,
) -> subprocess.CompletedProcess:
    """Execute file without throwing."""
    try:
        return subprocess.run(
            [command] + (args or []),
            capture_output=True,
            timeout=options.get("timeout") if options else None,
        )
    except Exception as e:
        return subprocess.CompletedProcess(
            args=[command] + (args or []),
            returncode=1,
            stdout="",
            stderr=str(e),
        )


__all__ = ["exec_file_no_throw"]