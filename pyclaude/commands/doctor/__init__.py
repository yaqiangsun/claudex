"""
Doctor command - check and fix Claude Code issues.
"""

from typing import Dict, Any


async def doctor_check() -> Dict[str, Any]:
    """Run doctor checks."""
    issues = []
    suggestions = []

    # Check Python version
    import sys
    if sys.version_info < (3, 9):
        issues.append("Python 3.9+ required")
    else:
        suggestions.append("Python version OK")

    # Check for required modules
    try:
        import click
        suggestions.append("click installed")
    except ImportError:
        issues.append("click not installed")

    try:
        import httpx
        suggestions.append("httpx installed")
    except ImportError:
        issues.append("httpx not installed")

    return {
        "type": "text",
        "value": "Doctor Check Results:\n\n" +
                 "Issues:\n" + "\n".join(f"  - {i}" for i in issues) + "\n\n" +
                 "Suggestions:\n" + "\n".join(f"  - {s}" for s in suggestions)
    }


__all__ = ["doctor_check"]