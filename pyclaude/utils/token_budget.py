"""
Token budget utilities.

Token budget tracking.
"""

from typing import Optional, Dict, Any


class TokenBudget:
    """Token budget tracker."""

    def __init__(self, max_tokens: int = 100000):
        self.max_tokens = max_tokens
        self.used_tokens = 0

    def allocate(self, tokens: int) -> bool:
        """Allocate tokens."""
        if self.used_tokens + tokens <= self.max_tokens:
            self.used_tokens += tokens
            return True
        return False

    def remaining(self) -> int:
        """Get remaining tokens."""
        return max(0, self.max_tokens - self.used_tokens)


_budget = TokenBudget()


def get_token_budget() -> TokenBudget:
    """Get global token budget."""
    return _budget


__all__ = [
    "TokenBudget",
    "get_token_budget",
]