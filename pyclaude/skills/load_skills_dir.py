"""Load Skills Directory - Enhanced to match src/skills/loadSkillsDir.ts"""
from __future__ import annotations
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from pyclaude.utils.frontmatter_parser import parse_frontmatter

# Memory types for skills
MEMORY_TYPES = ['user', 'feedback', 'project', 'reference']

# Type for loaded_from
LOADED_FROM_TYPES = ['commands_DEPRECATED', 'skills', 'plugin', 'managed', 'bundled', 'mcp']


@dataclass
class Skill:
    """Represents a loaded skill."""
    name: str
    description: str
    content: str
    file_path: str
    source: str
    loaded_from: str
    display_name: Optional[str] = None
    allowed_tools: list = field(default_factory=list)
    argument_hint: Optional[str] = None
    argument_names: list = field(default_factory=list)
    when_to_use: Optional[str] = None
    version: Optional[str] = None
    model: Optional[str] = None
    disable_model_invocation: bool = False
    user_invocable: bool = True
    is_hidden: bool = False
    paths: Optional[list] = None
    hooks: Optional[dict] = None
    context: Optional[str] = None
    agent: Optional[str] = None
    effort: Optional[str] = None
    shell: Optional[dict] = None
    skill_root: Optional[str] = None

    # For legacy commands
    has_user_specified_description: bool = False


def get_file_identity(file_path: str) -> Optional[str]:
    """Get a unique identifier for a file by resolving symlinks.

    Returns None if the file doesn't exist or can't be resolved.
    """
    try:
        return os.path.realpath(file_path)
    except OSError:
        return None


def parse_hooks_from_frontmatter(frontmatter: dict, skill_name: str) -> Optional[dict]:
    """Parse and validate hooks from frontmatter.

    Returns None if hooks are not defined or invalid.
    """
    if not frontmatter or 'hooks' not in frontmatter:
        return None

    hooks = frontmatter.get('hooks')

    # Basic validation - could be extended with HooksSchema
    if not isinstance(hooks, dict):
        return None

    return hooks


def parse_skill_paths(frontmatter: dict) -> Optional[list[str]]:
    """Parse paths frontmatter from a skill.

    Returns None if no paths are specified or if all patterns are match-all.
    """
    if not frontmatter or 'paths' not in frontmatter:
        return None

    paths_str = frontmatter['paths']

    if isinstance(paths_str, str):
        patterns = [p.strip() for p in paths_str.split('\n') if p.strip()]
    elif isinstance(paths_str, list):
        patterns = [str(p) for p in paths_str]
    else:
        return None

    # Remove /** suffix - ignore library treats 'path' as matching both
    # the path itself and everything inside it
    patterns = [p[:-3] if p.endswith('/**') else p for p in patterns]

    # Filter empty and match-all patterns
    patterns = [p for p in patterns if p and p != '**']

    if not patterns:
        return None

    return patterns


def parse_skill_frontmatter(frontmatter: dict, content: str, name: str) -> dict:
    """Parse skill frontmatter fields - enhanced version."""
    result = {}

    # Description - from frontmatter or extracted from content
    if frontmatter and 'description' in frontmatter:
        result['description'] = frontmatter['description']
        result['has_user_specified_description'] = True
    else:
        # Extract first paragraph as description
        lines = content.strip().split('\n')
        description = ''
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                description = line[:100]  # First 100 chars
                break
        result['description'] = description or f'{name} skill'
        result['has_user_specified_description'] = False

    # displayName
    if frontmatter and 'name' in frontmatter:
        result['display_name'] = str(frontmatter['name'])

    # allowedTools
    if frontmatter and 'allowed-tools' in frontmatter:
        tools_str = frontmatter['allowed-tools']
        if isinstance(tools_str, str):
            result['allowed_tools'] = [t.strip() for t in tools_str.split(',')]
        elif isinstance(tools_str, list):
            result['allowed_tools'] = tools_str
        else:
            result['allowed_tools'] = []
    else:
        result['allowed_tools'] = []

    # argumentHint
    if frontmatter and 'argument-hint' in frontmatter:
        result['argument_hint'] = str(frontmatter['argument-hint'])

    # argumentNames (from 'arguments' field)
    if frontmatter and 'arguments' in frontmatter:
        args_str = frontmatter['arguments']
        if isinstance(args_str, str):
            result['argument_names'] = [a.strip().strip('{}') for a in args_str.split(',')]
        elif isinstance(args_str, list):
            result['argument_names'] = [str(a).strip().strip('{}') for a in args_str]
        else:
            result['argument_names'] = []
    else:
        result['argument_names'] = []

    # whenToUse
    if frontmatter and 'when_to_use' in frontmatter:
        result['when_to_use'] = frontmatter['when_to_use']

    # version
    if frontmatter and 'version' in frontmatter:
        result['version'] = str(frontmatter['version'])

    # model
    if frontmatter and 'model' in frontmatter:
        model_val = frontmatter['model']
        if model_val == 'inherit':
            result['model'] = None
        elif model_val:
            result['model'] = str(model_val)

    # disableModelInvocation
    if frontmatter and 'disable-model-invocation' in frontmatter:
        val = frontmatter['disable-model-invocation']
        result['disable_model_invocation'] = str(val).lower() in ('true', '1', 'yes')

    # userInvocable - defaults to True
    if frontmatter and 'user-invocable' in frontmatter:
        val = frontmatter['user-invocable']
        result['user_invocable'] = str(val).lower() not in ('false', '0', 'no')
    else:
        result['user_invocable'] = True

    # context (execution context: fork)
    if frontmatter and 'context' in frontmatter:
        ctx = frontmatter['context']
        if ctx == 'fork':
            result['context'] = 'fork'

    # agent
    if frontmatter and 'agent' in frontmatter:
        result['agent'] = str(frontmatter['agent'])

    # effort
    if frontmatter and 'effort' in frontmatter:
        result['effort'] = str(frontmatter['effort'])

    # shell
    if frontmatter and 'shell' in frontmatter:
        result['shell'] = frontmatter['shell']

    # hooks
    result['hooks'] = parse_hooks_from_frontmatter(frontmatter, name)

    # paths (conditional skills)
    result['paths'] = parse_skill_paths(frontmatter)

    return result


def substitute_arguments(content: str, args: str, allow_empty: bool = True, arg_names: list = None) -> str:
    """Substitute arguments in skill content."""
    if not args:
        return content

    # Parse argument names if not provided
    if arg_names is None:
        # Try to extract from content
        arg_names = []

    # Simple substitution: $1, $2, etc. or ${arg_name}
    result = content

    # Replace positional arguments
    arg_list = args.split()
    for i, arg in enumerate(arg_list):
        result = result.replace(f'${i + 1}', arg)

    # Replace named arguments ${name}
    for arg_name in arg_names:
        # This is simplified - real implementation would parse args more carefully
        pass

    return result


def get_session_id() -> str:
    """Get the current session ID."""
    # Simplified - would integrate with actual session management
    return os.environ.get('CLAUDE_SESSION_ID', 'default')


def execute_shell_commands_in_prompt(content: str, skill_name: str = None) -> str:
    """Execute shell commands in prompt content.

    Supports:
    - !`command` syntax (inline)
    - ```! ... ``` code blocks

    Returns content with command output substituted.
    """
    # Inline shell: !`command`
    inline_pattern = re.compile(r'!`([^`]+)`')

    # Code block shell: ```! ... ```
    block_pattern = re.compile(r'```!?\n(.*?)```', re.DOTALL)

    result = content

    # Process inline commands
    def run_inline(match):
        cmd = match.group(1).strip()
        try:
            import subprocess
            proc = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return proc.stdout if proc.returncode == 0 else f"[Error: {proc.stderr}]"
        except Exception as e:
            return f"[Error: {str(e)}]"

    result = inline_pattern.sub(run_inline, result)

    # Process code blocks (simplified - just remove the ! marker)
    def process_block(match):
        block_content = match.group(1)
        # Remove leading ! from first line if present
        lines = block_content.split('\n')
        if lines and lines[0].strip().startswith('!'):
            lines[0] = lines[0].replace('!', '', 1)
        return '\n'.join(lines)

    result = block_pattern.sub(process_block, result)

    return result


def create_skill_from_content(
    skill_name: str,
    content: str,
    file_path: str,
    source: str,
    loaded_from: str,
    base_dir: str = None,
    is_skill_format: bool = True,
    description_fallback_label: str = 'Skill',
) -> Skill:
    """Create a Skill from markdown content."""
    # Parse frontmatter
    frontmatter, markdown_content = parse_frontmatter(content)

    # Parse frontmatter fields
    parsed = parse_skill_frontmatter(frontmatter or {}, markdown_content, skill_name)

    # Use directory as base_dir for SKILL.md format
    if is_skill_format and base_dir is None:
        base_dir = os.path.dirname(file_path)

    skill_root = base_dir

    # Apply variable substitution
    final_content = substitute_arguments(
        markdown_content,
        '',
        True,
        parsed.get('argument_names', []),
    )

    # Replace ${CLAUDE_SKILL_DIR}
    if skill_root:
        final_content = final_content.replace('${CLAUDE_SKILL_DIR}', skill_root)

    # Replace ${CLAUDE_SESSION_ID}
    final_content = final_content.replace('${CLAUDE_SESSION_ID}', get_session_id())

    # Execute shell commands (if not from MCP - MCP skills are untrusted)
    if loaded_from != 'mcp':
        final_content = execute_shell_commands_in_prompt(final_content, skill_name)

    # Prepend base directory if present
    if skill_root:
        final_content = f"Base directory for this skill: {skill_root}\n\n{final_content}"

    return Skill(
        name=skill_name,
        description=parsed.get('description', f'{skill_name} skill'),
        content=final_content,
        file_path=file_path,
        source=source,
        loaded_from=loaded_from,
        display_name=parsed.get('display_name'),
        allowed_tools=parsed.get('allowed_tools', []),
        argument_hint=parsed.get('argument_hint'),
        argument_names=parsed.get('argument_names', []),
        when_to_use=parsed.get('when_to_use'),
        version=parsed.get('version'),
        model=parsed.get('model'),
        disable_model_invocation=parsed.get('disable_model_invocation', False),
        user_invocable=parsed.get('user_invocable', True),
        is_hidden=not parsed.get('user_invocable', True),
        paths=parsed.get('paths'),
        hooks=parsed.get('hooks'),
        context=parsed.get('context'),
        agent=parsed.get('agent'),
        effort=parsed.get('effort'),
        shell=parsed.get('shell'),
        skill_root=skill_root,
        has_user_specified_description=parsed.get('has_user_specified_description', False),
    )


def load_skills_from_skills_dir(base_path: str, source: str = 'userSettings') -> list[Skill]:
    """Load skills from a /skills/ directory path.

    Only supports directory format: skill-name/SKILL.md
    """
    skills = []
    skills_path = Path(base_path)

    if not skills_path.exists() or not skills_path.is_dir():
        return skills

    try:
        entries = list(skills_path.iterdir())
    except PermissionError:
        return skills

    for entry in entries:
        # Only support directory format: skill-name/SKILL.md
        if not entry.is_dir():
            continue

        skill_file_path = entry / 'SKILL.md'

        if not skill_file_path.exists():
            continue

        try:
            content = skill_file_path.read_text(encoding='utf-8')
        except (PermissionError, OSError):
            continue

        skill_name = entry.name

        skill = create_skill_from_content(
            skill_name=skill_name,
            content=content,
            file_path=str(skill_file_path),
            source=source,
            loaded_from='skills',
            base_dir=str(entry),
            is_skill_format=True,
        )
        skills.append(skill)

    return skills


def is_skill_file(file_path: str) -> bool:
    """Check if a file is a SKILL.md file."""
    return Path(file_path).name.lower() == 'skill.md'


def get_command_name_from_path(file_path: str, base_dir: str) -> str:
    """Get command name from file path for legacy /commands/ format."""
    file_path = Path(file_path)
    base_dir = Path(base_dir)

    # Get the directory containing the command
    cmd_dir = file_path.parent

    # If it's a skill (SKILL.md), use parent directory name
    if is_skill_file(str(file_path)):
        cmd_dir = cmd_dir.parent

    # Calculate relative path from base_dir
    if cmd_dir == base_dir:
        namespace = ''
    else:
        try:
            rel_path = cmd_dir.relative_to(base_dir)
            namespace = str(rel_path).replace(os.sep, ':')
        except ValueError:
            namespace = ''

    # Get command base name
    if is_skill_file(str(file_path)):
        command_base_name = file_path.parent.name
    else:
        command_base_name = file_path.stem

    return f"{namespace}:{command_base_name}" if namespace else command_base_name


def load_skills_from_commands_dir(cwd: str) -> list[Skill]:
    """Load skills from legacy /commands/ directories.

    Supports both directory format (SKILL.md) and single .md file format.
    """
    skills = []
    commands_path = Path(cwd) / '.claude' / 'commands'

    if not commands_path.exists():
        return skills

    try:
        # Walk through all .md files
        for md_file in commands_path.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
            except (PermissionError, OSError):
                continue

            # Determine if it's SKILL.md format or regular command
            is_skill = is_skill_file(str(md_file))

            # Get command name
            cmd_name = get_command_name_from_path(
                str(md_file),
                str(commands_path),
            )

            # Base directory for skill
            base_dir = str(md_file.parent) if is_skill else None

            skill = create_skill_from_content(
                skill_name=cmd_name,
                content=content,
                file_path=str(md_file),
                source='projectSettings',
                loaded_from='commands_DEPRECATED',
                base_dir=base_dir,
                is_skill_format=is_skill,
                description_fallback_label='Custom command',
            )

            # Commands default to user-invocable: true
            skill.user_invocable = True
            skill.is_hidden = False

            skills.append(skill)

    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error loading commands: {e}")

    return skills


def load_skills_dir(skills_dir: str | Path) -> list[dict[str, Any]]:
    """Load skills from a directory.

    Returns a list of skill dictionaries (legacy format for compatibility).
    """
    if isinstance(skills_dir, str):
        skills_dir = Path(skills_dir)

    skills = load_skills_from_skills_dir(str(skills_dir))

    # Convert to legacy dict format
    return [
        {
            'name': s.name,
            'description': s.description,
            'content': s.content,
            'path': s.file_path,
            'source': s.source,
            'loaded_from': s.loaded_from,
        }
        for s in skills
    ]


# --- Dynamic skill state ---
_dynamic_skill_dirs: set = set()
_dynamic_skills: dict[str, Skill] = {}
_conditional_skills: dict[str, Skill] = {}
_activated_conditional_skill_names: set = set()


def discover_skill_dirs_for_paths(file_paths: list[str], cwd: str) -> list[str]:
    """Discover skill directories by walking up from file paths to cwd.

    Only discovers directories below cwd (cwd-level skills are loaded at startup).
    """
    resolved_cwd = cwd.rstrip(os.sep)
    new_dirs = []

    for file_path in file_paths:
        # Start from the file's parent directory
        current_dir = os.path.dirname(file_path)

        # Walk up to cwd but NOT including cwd itself
        while current_dir.startswith(resolved_cwd + os.sep):
            skill_dir = os.path.join(current_dir, '.claude', 'skills')

            # Skip if we've already checked this path
            if skill_dir not in _dynamic_skill_dirs:
                _dynamic_skill_dirs.add(skill_dir)

                if os.path.isdir(skill_dir):
                    new_dirs.append(skill_dir)

            # Move to parent
            parent = os.path.dirname(current_dir)
            if parent == current_dir:
                break
            current_dir = parent

    # Sort by path depth (deepest first)
    new_dirs.sort(key=lambda d: d.count(os.sep), reverse=True)
    return new_dirs


def add_skill_directories(dirs: list[str]) -> None:
    """Load skills from the given directories and merge into dynamic skills."""
    if not dirs:
        return

    # Load skills from all directories
    for dir_path in dirs:
        loaded_skills = load_skills_from_skills_dir(dir_path, 'projectSettings')

        # Add to dynamic skills (deeper paths override)
        for skill in loaded_skills:
            if skill.name:
                _dynamic_skills[skill.name] = skill


def activate_conditional_skills_for_paths(file_paths: list[str], cwd: str) -> list[str]:
    """Activate conditional skills whose path patterns match the given file paths."""
    if not _conditional_skills:
        return []

    activated = []

    # Import ignore for pattern matching
    try:
        import ignore
    except ImportError:
        return []

    for name, skill in list(_conditional_skills.items()):
        if not skill.paths or not skill.paths:
            continue

        # Create ignore matcher
        skill_ignore = ignore.Ignore().add(skill.paths)

        for file_path in file_paths:
            # Calculate relative path
            if os.path.isabs(file_path):
                try:
                    relative_path = os.path.relpath(file_path, cwd)
                except ValueError:
                    continue
            else:
                relative_path = file_path

            # Skip paths outside cwd
            if not relative_path or relative_path.startswith('..') or os.path.isabs(relative_path):
                continue

            if skill_ignore.ignores(relative_path):
                # Activate this skill
                _dynamic_skills[name] = skill
                del _conditional_skills[name]
                _activated_conditional_skill_names.add(name)
                activated.append(name)
                break

    return activated


def get_dynamic_skills() -> list[Skill]:
    """Get all dynamically discovered skills."""
    return list(_dynamic_skills.values())


def get_conditional_skill_count() -> int:
    """Get the number of pending conditional skills."""
    return len(_conditional_skills)


def clear_dynamic_skills() -> None:
    """Clear dynamic skill state."""
    _dynamic_skill_dirs.clear()
    _dynamic_skills.clear()
    _conditional_skills.clear()
    _activated_conditional_skill_names.clear()


def get_skills_dir_commands(cwd: str = None) -> list[Skill]:
    """Load all skills from all configured directories.

    Loads from:
    - User skills: ~/.claude/skills
    - Project skills: .claude/skills in cwd and parents
    - Managed skills: ~/.claude-managed/.claude/skills
    - Legacy commands: .claude/commands in cwd

    Args:
        cwd: Current working directory for project skills

    Returns:
        List of all loaded skills
    """
    from pyclaude.utils.env_utils import get_claude_config_home_dir, get_managed_file_path

    all_skills = []
    seen_paths = set()

    # User skills
    user_skills_dir = Path(get_claude_config_home_dir()) / 'skills'
    user_skills = load_skills_from_skills_dir(str(user_skills_dir), 'userSettings')

    # Deduplicate by resolved path
    for skill in user_skills:
        file_id = get_file_identity(skill.file_path)
        if file_id and file_id not in seen_paths:
            seen_paths.add(file_id)
            all_skills.append(skill)

    # Managed skills
    managed_skills_dir = Path(get_managed_file_path()) / '.claude' / 'skills'
    managed_skills = load_skills_from_skills_dir(str(managed_skills_dir), 'policySettings')

    for skill in managed_skills:
        file_id = get_file_identity(skill.file_path)
        if file_id and file_id not in seen_paths:
            seen_paths.add(file_id)
            all_skills.append(skill)

    # Project skills (if cwd provided)
    if cwd:
        project_skills = load_project_skills(cwd)
        for skill in project_skills:
            file_id = get_file_identity(skill.file_path)
            if file_id and file_id not in seen_paths:
                seen_paths.add(file_id)
                all_skills.append(skill)

        # Legacy commands
        legacy_commands = load_skills_from_commands_dir(cwd)
        for skill in legacy_commands:
            file_id = get_file_identity(skill.file_path)
            if file_id and file_id not in seen_paths:
                seen_paths.add(file_id)
                all_skills.append(skill)

    # Separate conditional skills
    unconditional_skills = []
    new_conditional_skills = []

    for skill in all_skills:
        if skill.paths and skill.paths not in ([], None):
            if skill.name not in _activated_conditional_skill_names:
                new_conditional_skills.append(skill)
            else:
                unconditional_skills.append(skill)
        else:
            unconditional_skills.append(skill)

    # Store conditional skills for later activation
    for skill in new_conditional_skills:
        _conditional_skills[skill.name] = skill

    return unconditional_skills


def load_project_skills(cwd: str) -> list[Skill]:
    """Load skills from project .claude/skills directories.

    Walks up from cwd to home directory, loading .claude/skills from each level.
    """
    from pyclaude.utils.env_utils import get_project_dirs_up_to_home

    skills = []
    project_dirs = get_project_dirs_up_to_home('skills', cwd)

    for project_dir in project_dirs:
        project_skills_dir = Path(project_dir) / '.claude' / 'skills'
        project_skills = load_skills_from_skills_dir(str(project_skills_dir), 'projectSettings')
        skills.extend(project_skills)

    return skills


def clear_skill_caches() -> None:
    """Clear skill caches (for testing)."""
    clear_dynamic_skills()


__all__ = [
    'Skill',
    'load_skills_dir',
    'load_skills_from_dir',
    'load_skills_from_skills_dir',
    'load_skills_from_commands_dir',
    'get_skills_dir_commands',
    'load_project_skills',
    'get_file_identity',
    'parse_skill_frontmatter',
    'substitute_arguments',
    'execute_shell_commands_in_prompt',
    'create_skill_from_content',
    'discover_skill_dirs_for_paths',
    'add_skill_directories',
    'activate_conditional_skills_for_paths',
    'get_dynamic_skills',
    'get_conditional_skill_count',
    'clear_dynamic_skills',
    'clear_skill_caches',
]