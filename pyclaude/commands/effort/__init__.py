"""
Effort command - set reasoning effort level.
"""

from typing import Dict, Any


EFFORT_LEVELS = {
    "minimum": "Use minimal reasoning for simple tasks",
    "medium": "Use balanced reasoning effort",
    "maximum": "Use maximum reasoning for complex tasks",
}


async def handle_effort(args: str, context: Any) -> Dict[str, Any]:
    """Handle effort command."""
    args = args.strip().lower()

    if not args:
        # Show current effort
        current = context.get_app_state().effort if hasattr(context, 'get_app_state') else "medium"
        return {
            "type": "text",
            "value": f"Current effort: {current}\n\nAvailable: " + ", ".join(EFFORT_LEVELS.keys()),
        }

    if args in EFFORT_LEVELS:
        return {
            "type": "text",
            "value": f"Effort set to: {args}\n{EFFORT_LEVELS[args]}",
        }

    return {
        "type": "text",
        "value": f"Unknown effort level: {args}\n\nAvailable: " + ", ".join(EFFORT_LEVELS.keys()),
    }


__all__ = ["handle_effort", "EFFORT_LEVELS"]