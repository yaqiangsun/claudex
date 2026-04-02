"""Memory scan utilities."""
import os
from pathlib import Path


def scan_memories(memory_dir: str) -> list[dict]:
    """Scan memory directory for memory files."""
    memories = []
    memory_path = Path(memory_dir)

    if not memory_path.exists():
        return memories

    # TODO: implement actual scanning
    return memories


def find_relevant_memories(memory_dir: str, query: str) -> list[dict]:
    """Find memories relevant to a query."""
    # TODO: implement actual search
    return []


__all__ = ['scan_memories', 'find_relevant_memories']