"""
User prompt keywords utilities.

Extract keywords from user prompts.
"""

from typing import List


def extract_keywords(prompt: str) -> List[str]:
    """Extract keywords from prompt."""
    words = prompt.lower().split()
    # Simple keyword extraction - would be more sophisticated in real implementation
    return [w for w in words if len(w) > 3][:10]


__all__ = ["extract_keywords"]