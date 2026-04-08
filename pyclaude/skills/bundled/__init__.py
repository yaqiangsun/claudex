"""Bundled Skills - Python implementation matching src/skills/bundled/"""
from __future__ import annotations

# Re-export from bundled_skills module
from pyclaude.skills.bundled_skills import (
    BundledSkillDefinition,
    register_bundled_skill,
    get_bundled_skill,
    get_all_bundled_skills,
    clear_bundled_skills,
    get_bundled_skills_root,
    get_bundled_skill_extract_dir,
    extract_bundled_skill_files,
    resolve_skill_file_path,
    prepend_base_dir,
    has_feature,
    is_ant_user,
    is_auto_memory_enabled,
    _bundled_skills as _internal_skills,
)

# BUNDLED_SKILLS is a reference to the internal dict for backwards compatibility
BUNDLED_SKILLS = _internal_skills


def _should_auto_enable_claude_in_chrome() -> bool:
    """Check if Claude in Chrome should be auto-enabled."""
    # Simplified implementation - check for Chrome browser
    import sys
    import shutil

    # Check if Chrome is installed
    if sys.platform == 'darwin':
        return shutil.which('google-chrome') is not None or \
               shutil.which('Google Chrome') is not None
    elif sys.platform == 'linux':
        return shutil.which('google-chrome') is not None
    elif sys.platform == 'win32':
        return shutil.which('chrome.exe') is not None
    return False


def init_bundled_skills() -> None:
    """Initialize all bundled skills with feature flags."""
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
    )

    # Core skills - always registered
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

    # Feature-gated skills
    if has_feature('AGENT_TRIGGERS'):
        from pyclaude.skills.bundled import loop
        loop.register()

    if has_feature('AGENT_TRIGGERS_REMOTE'):
        from pyclaude.skills.bundled import schedule_remote_agents
        schedule_remote_agents.register()

    if has_feature('BUILDING_CLAUDE_APPS'):
        from pyclaude.skills.bundled import claude_api
        claude_api.register()

    # claude-in-chrome is conditionally enabled based on Chrome setup
    if _should_auto_enable_claude_in_chrome():
        from pyclaude.skills.bundled import claude_in_chrome
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
    'get_bundled_skills_root',
    'get_bundled_skill_extract_dir',
    'extract_bundled_skill_files',
    'has_feature',
]