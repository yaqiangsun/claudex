"""Formatters for LSPTool matching src/tools/LSPTool/formatters.ts"""
from typing import Dict, Any, List


# Supported formatters by language
FORMATTERS = {
    "python": ["ruff", "black", "yapf"],
    "javascript": ["prettier", "eslint"],
    "typescript": ["prettier", "eslint"],
    "rust": ["rustfmt"],
    "go": ["gofmt", "goimports"],
    "java": ["google-java-format"],
    "css": ["prettier"],
    "json": ["prettier"],
    "markdown": ["prettier"],
}


def get_formatter(language: str) -> List[str]:
    """Get available formatters for a language."""
    return FORMATTERS.get(language.lower(), [])


def is_formatter_available(formatter: str) -> bool:
    """Check if a formatter is available on the system."""
    import shutil
    return shutil.which(formatter) is not None


__all__ = ["FORMATTERS", "get_formatter", "is_formatter_available"]