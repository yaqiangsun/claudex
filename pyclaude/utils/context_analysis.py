"""
Context analysis utility.
"""
from typing import Dict, Any

def analyze_context(context: Dict[str, Any]) -> Dict[str, Any]:
    return {'size': len(str(context)), 'keys': list(context.keys())}

__all__ = ['analyze_context']