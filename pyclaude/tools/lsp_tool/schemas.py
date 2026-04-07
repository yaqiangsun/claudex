"""Schemas for LSPTool matching src/tools/LSPTool/schemas.ts"""
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class SymbolInfo:
    """Information about a code symbol."""
    name: str
    kind: str
    location: str
    container: str = ""


# Symbol kinds
SYMBOL_KINDS = {
    "file": 1,
    "module": 2,
    "namespace": 3,
    "package": 4,
    "class": 5,
    "method": 6,
    "property": 7,
    "field": 8,
    "constructor": 9,
    "enum": 10,
    "interface": 11,
    "function": 12,
    "variable": 13,
    "constant": 14,
    "string": 15,
    "number": 16,
    "boolean": 17,
    "array": 18,
}


def get_symbol_kind(name: str) -> int:
    """Get symbol kind ID by name."""
    return SYMBOL_KINDS.get(name.lower(), 0)


__all__ = ["SymbolInfo", "SYMBOL_KINDS", "get_symbol_kind"]