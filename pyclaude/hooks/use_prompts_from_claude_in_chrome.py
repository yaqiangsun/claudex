"""Hook for prompts from Claude in Chrome."""


class PromptsFromClaudeInChrome:
    """Manages prompts integration from Claude in Chrome."""

    def __init__(self):
        self._prompts = []
        self._enabled = False

    def enable(self) -> None:
        """Enable Chrome prompts integration."""
        self._enabled = True

    def disable(self) -> None:
        """Disable Chrome prompts integration."""
        self._enabled = False

    def is_enabled(self) -> bool:
        """Check if Chrome prompts are enabled."""
        return self._enabled

    def add_prompt(self, prompt: str) -> None:
        """Add a prompt from Chrome."""
        self._prompts.append(prompt)

    def get_prompts(self) -> list:
        """Get all prompts."""
        return self._prompts.copy()


__all__ = ['PromptsFromClaudeInChrome']