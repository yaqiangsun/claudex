"""
Doctor context warnings utility.
"""
from typing import List, Dict, Any

def get_context_warnings() -> List[str]:
    return []

def check_context_issues(context: Dict[str, Any]) -> List[str]:
    return []

__all__ = ['get_context_warnings', 'check_context_issues']