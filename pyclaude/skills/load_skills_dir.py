"""Load Skills Directory."""
from pathlib import Path
from typing import Any


def load_skills_dir(skills_dir: str | Path) -> list[dict[str, Any]]:
    """Load skills from a directory."""
    skills = []
    skills_path = Path(skills_dir)

    if not skills_path.exists():
        return skills

    # TODO: implement actual loading
    return skills


__all__ = ['load_skills_dir']