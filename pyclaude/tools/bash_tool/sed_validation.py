"""Sed validation matching src/tools/BashTool/sedValidation.ts"""
import re
from typing import Dict, Any


# Dangerous sed patterns
DANGEROUS_SED_PATTERNS = [
    (r's/.*/.*/g', 'Global replacement may affect multiple files'),
    (r's/\s*//g', 'Removing all whitespace'),
    (r'/^\s*$/d', 'Deleting empty lines'),
]


def validate_sed_command(command: str) -> Dict[str, Any]:
    """Validate sed command for safety."""
    warnings = []
    is_safe = True

    # Extract sed part from command
    sed_match = re.search(r"sed\s+['\"]([^'\"]+)['\"]", command)
    if not sed_match:
        return {"valid": True, "warnings": []}

    sed_cmd = sed_match.group(1)

    # Check for dangerous patterns
    for pattern, description in DANGEROUS_SED_PATTERNS:
        if re.search(pattern, sed_cmd):
            warnings.append(description)
            is_safe = False

    return {
        "valid": is_safe,
        "warnings": warnings,
    }


def is_sed_safe(command: str) -> bool:
    """Quick check if sed command is safe."""
    result = validate_sed_command(command)
    return result["valid"]


__all__ = ["DANGEROUS_SED_PATTERNS", "validate_sed_command", "is_sed_safe"]