"""Bundled Skills."""
from typing import Any, Callable

# Bundled skill definition
class BundledSkillDefinition:
    def __init__(
        self,
        name: str,
        description: str,
        allowed_tools: list[str] | None = None,
        argument_hint: str | None = None,
        when_to_use: str | None = None,
        model: str | None = None,
        disable_model_invocation: bool = False,
        user_invocable: bool = True,
        hooks: list | None = None,
        context: dict | None = None,
        agent: dict | None = None,
        is_enabled: Callable[[], bool] | None = None,
        get_prompt_for_command: Callable | None = None,
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


def get_bundled_skill(name: str) -> BundledSkillDefinition | None:
    """Get a bundled skill by name."""
    return BUNDLED_SKILLS.get(name)


def get_all_bundled_skills() -> list[BundledSkillDefinition]:
    """Get all bundled skills."""
    return list(BUNDLED_SKILLS.values())


__all__ = [
    'BundledSkillDefinition',
    'BUNDLED_SKILLS',
    'register_bundled_skill',
    'get_bundled_skill',
    'get_all_bundled_skills',
]