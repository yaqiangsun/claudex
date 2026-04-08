"""Bundled Skills - Core registry and definition matching src/skills/bundledSkills.ts"""
from __future__ import annotations
import os
import asyncio
from pathlib import Path
from typing import Any, Callable, Optional

# Bundled skill definition
class BundledSkillDefinition:
    def __init__(
        self,
        name: str,
        description: str,
        aliases: Optional[list[str]] = None,
        allowed_tools: Optional[list[str]] = None,
        argument_hint: Optional[str] = None,
        when_to_use: Optional[str] = None,
        model: Optional[str] = None,
        disable_model_invocation: bool = False,
        user_invocable: bool = True,
        hooks: Optional[list] = None,
        context: Optional[dict] = None,
        agent: Optional[dict] = None,
        is_enabled: Optional[Callable[[], bool]] = None,
        get_prompt_for_command: Optional[Callable] = None,
        files: Optional[dict[str, str]] = None,
    ):
        self.name = name
        self.description = description
        self.aliases = aliases or []
        self.allowed_tools = allowed_tools or []
        self.argument_hint = argument_hint
        self.when_to_use = when_to_use
        self.model = model
        self.disable_model_invocation = disable_model_invocation
        self.user_invocable = user_invocable
        self.hooks = hooks or []
        self.context = context or {}
        self.agent = agent
        self.is_enabled = is_enabled or (lambda: True)
        self.get_prompt_for_command = get_prompt_for_command
        self.files = files or {}


# Internal registry for bundled skills
_bundled_skills: dict[str, BundledSkillDefinition] = {}


def register_bundled_skill(definition: BundledSkillDefinition) -> None:
    """Register a bundled skill that will be available to the model.

    Bundled skills are compiled into the CLI binary and available to all users.
    """
    _bundled_skills[definition.name] = definition


def get_bundled_skill(name: str) -> Optional[BundledSkillDefinition]:
    """Get a bundled skill by name."""
    return _bundled_skills.get(name)


def get_all_bundled_skills() -> list[BundledSkillDefinition]:
    """Get all registered bundled skills.

    Returns a copy to prevent external mutation.
    """
    return list(_bundled_skills.values())


def clear_bundled_skills() -> None:
    """Clear bundled skills registry (for testing)."""
    _bundled_skills.clear()


def get_bundled_skills_root() -> str:
    """Get the root directory for bundled skill extraction."""
    # This would use a proper path in the actual implementation
    return os.path.join(os.path.expanduser('~'), '.cache', 'pyclaude', 'skills')


def get_bundled_skill_extract_dir(skill_name: str) -> str:
    """Deterministic extraction directory for a bundled skill's reference files."""
    return os.path.join(get_bundled_skills_root(), skill_name)


def is_ant_user() -> bool:
    """Check if the current user is an ant (internal user)."""
    return os.environ.get('USER_TYPE') == 'ant'


def is_auto_memory_enabled() -> bool:
    """Check if auto-memory is enabled."""
    try:
        from pyclaude.memdir.paths import isAutoMemoryEnabled
        return isAutoMemoryEnabled()
    except ImportError:
        return False


# Feature flags (simplified version)
def has_feature(name: str) -> bool:
    """Check if a feature flag is enabled."""
    # Check environment variables for features
    feature_env = os.environ.get('CLAUDE_FEATURES', '')
    if name in feature_env.split(','):
        return True
    # Check individual feature env vars
    return os.environ.get(f'CLAUDE_FEATURE_{name.upper()}') == '1'


# File extraction for bundled skills
async def extract_bundled_skill_files(
    skill_name: str,
    files: dict[str, str],
) -> str | None:
    """Extract a bundled skill's reference files to disk.

    Returns the directory written to, or None if write failed.
    """
    import tempfile

    dir_path = get_bundled_skill_extract_dir(skill_name)

    try:
        # Create directory with restricted permissions
        os.makedirs(dir_path, mode=0o700, exist_ok=True)

        for rel_path, content in files.items():
            target_path = resolve_skill_file_path(dir_path, rel_path)

            # Create parent directories
            parent_dir = os.path.dirname(target_path)
            if parent_dir:
                os.makedirs(parent_dir, mode=0o700, exist_ok=True)

            # Write file with restricted permissions
            # Use exclusive create to prevent symlink attacks
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
            try:
                fd = os.open(target_path, flags, 0o600)
                try:
                    os.write(fd, content.encode('utf-8'))
                finally:
                    os.close(fd)
            except FileExistsError:
                # File already exists, skip
                pass

        return dir_path
    except Exception as e:
        import logging
        logging.getLogger(__name__).debug(
            f"Failed to extract bundled skill '{skill_name}' to {dir_path}: {e}"
        )
        return None


def resolve_skill_file_path(base_dir: str, rel_path: str) -> str:
    """Normalize and validate a skill-relative path; throws on traversal."""
    # Normalize the path
    normalized = os.path.normpath(rel_path)

    # Check for absolute paths or traversal
    if os.path.isabs(normalized):
        raise ValueError(f"bundled skill file path escapes skill dir: {rel_path}")

    # Check for .. traversal
    parts = normalized.split(os.sep)
    if '..' in parts:
        raise ValueError(f"bundled skill file path escapes skill dir: {rel_path}")

    return os.path.join(base_dir, normalized)


def prepend_base_dir(blocks: list[dict], base_dir: str) -> list[dict]:
    """Prepend base directory to content blocks."""
    prefix = f"Base directory for this skill: {base_dir}\n\n"

    if blocks and blocks[0].get('type') == 'text':
        blocks = [{'type': 'text', 'text': prefix + blocks[0].get('text', '')}] + blocks[1:]
    else:
        blocks = [{'type': 'text', 'text': prefix}] + blocks

    return blocks


__all__ = [
    'BundledSkillDefinition',
    'register_bundled_skill',
    'get_bundled_skill',
    'get_all_bundled_skills',
    'clear_bundled_skills',
    'get_bundled_skills_root',
    'get_bundled_skill_extract_dir',
    'extract_bundled_skill_files',
    'resolve_skill_file_path',
    'prepend_base_dir',
    'has_feature',
    'is_ant_user',
    'is_auto_memory_enabled',
]