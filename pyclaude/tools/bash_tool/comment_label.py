"""Comment label matching src/tools/BashTool/commentLabel.ts"""
import re
from typing import Optional


# Labels that indicate special command types
COMMENT_LABELS = {
    'CREATE': 'Creating new files or directories',
    'DELETE': 'Deleting files or directories',
    'MODIFY': 'Modifying existing files',
    'INSTALL': 'Installing packages or dependencies',
    'RUN': 'Running commands or scripts',
    'COMPILE': 'Compiling code',
    'TEST': 'Running tests',
    'DEPLOY': 'Deploying or releasing',
}


def extract_comment_label(command: str) -> Optional[str]:
    """Extract comment label from command."""
    # Look for # LABEL: pattern
    match = re.search(r'#\s*(\w+):', command)
    if match:
        label = match.group(1).upper()
        if label in COMMENT_LABELS:
            return label
    return None


def strip_comment_label(command: str) -> str:
    """Remove comment label from command."""
    return re.sub(r'#\s*\w+:\s*', '', command)


__all__ = ["COMMENT_LABELS", "extract_comment_label", "strip_comment_label"]