"""Bundled Skills - Python implementation matching src/skills/bundled/"""
from __future__ import annotations
import os
from typing import Any, Callable, Optional

# Bundled skill definition
class BundledSkillDefinition:
    def __init__(
        self,
        name: str,
        description: str,
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
    ):
        self.name = name
        self.description = description
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


# Registry of bundled skills
BUNDLED_SKILLS: dict[str, BundledSkillDefinition] = {}


def register_bundled_skill(skill: BundledSkillDefinition) -> None:
    """Register a bundled skill."""
    BUNDLED_SKILLS[skill.name] = skill


def get_bundled_skill(name: str) -> Optional[BundledSkillDefinition]:
    """Get a bundled skill by name."""
    return BUNDLED_SKILLS.get(name)


def get_all_bundled_skills() -> list[BundledSkillDefinition]:
    """Get all bundled skills."""
    return list(BUNDLED_SKILLS.values())


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


def init_bundled_skills() -> None:
    """Initialize all bundled skills."""
    # Import and register each skill
    from pyclaude.skills.bundled import (
        update_config,
        debug,
        keybindings,
        verify,
        lorem_ipsum,
        skillify,
        remember,
        simplify,
        batch,
        stuck,
        loop,
        schedule_remote_agents,
        claude_api,
        claude_in_chrome,
    )

    update_config.register()
    debug.register()
    keybindings.register()
    verify.register()
    lorem_ipsum.register()
    skillify.register()
    remember.register()
    simplify.register()
    batch.register()
    stuck.register()
    loop.register()
    schedule_remote_agents.register()
    claude_api.register()

    # claude-in-chrome is conditionally enabled based on Chrome setup
    claude_in_chrome.register()


# Auto-initialize on import
init_bundled_skills()


__all__ = [
    'BundledSkillDefinition',
    'BUNDLED_SKILLS',
    'register_bundled_skill',
    'get_bundled_skill',
    'get_all_bundled_skills',
    'init_bundled_skills',
    'is_ant_user',
    'is_auto_memory_enabled',
]