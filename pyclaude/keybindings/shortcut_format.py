"""Format shortcut display."""


def format_shortcut(key: str, modifiers: list[str] | None = None) -> str:
    """Format a shortcut for display."""
    parts = modifiers or []
    parts.append(key)
    return '+'.join(parts)


__all__ = ['format_shortcut']