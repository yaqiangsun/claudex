"""Files command - manage files."""

import os
import shutil
from pathlib import Path
from typing import Any, Dict


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the files command."""
    args = args.strip().lower() if args else ''

    if not args or args == 'list':
        return await list_files()

    if args.startswith('size '):
        path = args[5:].strip()
        return await show_file_size(path)

    if args.startswith('find '):
        pattern = args[5:].strip()
        return await find_files(pattern)

    return {'type': 'text', 'value': '''Usage: /files [command]

Commands:
  list              - List recent files
  size <path>       - Show file/directory size
  find <pattern>    - Find files matching pattern
'''}


async def list_files() -> Dict[str, Any]:
    """List recent files."""
    cwd = os.getcwd()
    files = []

    # Get recently modified files
    for root, dirs, filenames in os.walk(cwd):
        for f in filenames:
            if not f.startswith('.'):
                try:
                    path = Path(root) / f
                    mtime = path.stat().st_mtime
                    files.append((mtime, str(path)))
                except Exception:
                    pass

    # Sort by modification time
    files.sort(reverse=True)

    lines = ['Recent files:']
    for mtime, path in files[:20]:
        rel_path = os.path.relpath(path, cwd)
        lines.append(f'  {rel_path}')

    return {'type': 'text', 'value': '\n'.join(lines)}


async def show_file_size(path: str) -> Dict[str, Any]:
    """Show file size."""
    p = Path(path)

    if not p.exists():
        return {'type': 'text', 'value': f'Path not found: {path}'}

    if p.is_file():
        size = p.stat().st_size
        return {'type': 'text', 'value': f'{path}: {format_size(size)}'}

    # Directory
    total = 0
    for root, dirs, files in os.walk(p):
        for f in files:
            try:
                total += (Path(root) / f).stat().st_size
            except Exception:
                pass

    return {'type': 'text', 'value': f'{path}: {format_size(total)}'}


async def find_files(pattern: str) -> Dict[str, Any]:
    """Find files matching pattern."""
    from ...tools.glob_tool import GlobTool

    tool = GlobTool()
    result = await tool.execute(
        {'pattern': f'**/*{pattern}*'},
        lambda: {},
        lambda x: x,
    )

    files = result.get('files', [])
    if not files:
        return {'type': 'text', 'value': f'No files found matching: {pattern}'}

    lines = [f'Found {len(files)} files:']
    for f in files[:50]:
        lines.append(f'  {f}')

    return {'type': 'text', 'value': '\n'.join(lines)}


def format_size(size: int) -> str:
    """Format file size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f'{size:.1f} {unit}'
        size /= 1024
    return f'{size:.1f} PB'


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'files',
    'description': 'Manage files',
    'supports_non_interactive': True,
}


call = execute