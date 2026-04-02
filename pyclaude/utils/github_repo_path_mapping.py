"""
GitHub repo path mapping utilities.

Map GitHub repos to local paths.
"""

from typing import Dict, Optional


_repo_mapping: Dict[str, str] = {}


def add_repo_mapping(owner_repo: str, local_path: str) -> None:
    """Add repo to path mapping."""
    _repo_mapping[owner_repo.lower()] = local_path


def get_repo_path(owner_repo: str) -> Optional[str]:
    """Get local path for repo."""
    return _repo_mapping.get(owner_repo.lower())


def remove_repo_mapping(owner_repo: str) -> None:
    """Remove repo mapping."""
    _repo_mapping.pop(owner_repo.lower(), None)


__all__ = [
    "add_repo_mapping",
    "get_repo_path",
    "remove_repo_mapping",
]