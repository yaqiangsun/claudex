"""
Attachments utility.

Handle file attachments.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Attachment:
    """Represents a file attachment."""
    path: str
    name: str
    mime_type: Optional[str] = None
    size: Optional[int] = None


def create_attachment(path: str, name: Optional[str] = None) -> Attachment:
    """Create an attachment from a file path."""
    import os
    return Attachment(
        path=path,
        name=name or os.path.basename(path),
    )


def get_attachment_mime_type(path: str) -> Optional[str]:
    """Get MIME type for a file."""
    import mimetypes
    return mimetypes.guess_type(path)[0]


def validate_attachment(attachment: Attachment) -> bool:
    """Validate an attachment."""
    import os
    return os.path.exists(attachment.path)


__all__ = ['Attachment', 'create_attachment', 'get_attachment_mime_type', 'validate_attachment']