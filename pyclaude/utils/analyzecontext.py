"""
Analyze context utility.

Context analysis utilities.
"""

from typing import Dict, Any, List, Optional


def analyze_context(context: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze context and return insights."""
    return {
        'has_messages': 'messages' in context,
        'has_tools': 'tools' in context,
        'message_count': len(context.get('messages', [])),
        'tool_count': len(context.get('tools', [])),
    }


def extract_context_keywords(context: Dict[str, Any]) -> List[str]:
    """Extract keywords from context."""
    keywords = []
    messages = context.get('messages', [])
    for msg in messages:
        if isinstance(msg, dict):
            content = msg.get('content', '')
            if isinstance(content, str):
                keywords.extend(content.split()[:10])
    return keywords[:20]


def calculate_context_size(context: Dict[str, Any]) -> int:
    """Calculate approximate context size in tokens."""
    import json
    return len(json.dumps(context)) // 4  # rough estimate


__all__ = ['analyze_context', 'extract_context_keywords', 'calculate_context_size']