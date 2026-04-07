"""Attachments matching src/tools/BriefTool/attachments.ts"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import os


@dataclass
class Attachment:
    """A file attachment."""
    path: str
    name: str
    size: int
    mime_type: str = "application/octet-stream"


def parse_attachments(paths: List[str]) -> List[Attachment]:
    """Parse file paths into attachments."""
    attachments = []

    for path in paths:
        if os.path.exists(path):
            stat = os.stat(path)
            name = os.path.basename(path)
            # Simple mime type detection
            ext = os.path.splitext(path)[1].lower()
            mime_type = {
                '.txt': 'text/plain',
                '.md': 'text/markdown',
                '.py': 'text/x-python',
                '.js': 'text/javascript',
                '.ts': 'text/typescript',
                '.json': 'application/json',
                '.html': 'text/html',
                '.css': 'text/css',
            }.get(ext, 'application/octet-stream')

            attachments.append(Attachment(
                path=path,
                name=name,
                size=stat.st_size,
                mime_type=mime_type,
            ))

    return attachments


def validate_attachments(paths: List[str], max_size: int = 10 * 1024 * 1024) -> Dict[str, Any]:
    """Validate attachments."""
    errors = []
    warnings = []

    for path in paths:
        if not os.path.exists(path):
            errors.append(f"File not found: {path}")
            continue

        size = os.path.getsize(path)
        if size > max_size:
            warnings.append(f"File too large: {path} ({size} bytes)")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


__all__ = ["Attachment", "parse_attachments", "validate_attachments"]