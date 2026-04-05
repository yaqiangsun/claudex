"""Interactive helpers for user input."""
from typing import Optional, List, Dict, Any, Callable
import sys


class InteractiveHelper:
    """Helper for interactive user inputs."""

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}

    def register_handler(self, name: str, handler: Callable) -> None:
        """Register an input handler."""
        self._handlers[name] = handler

    def handle_input(self, name: str, **kwargs) -> Any:
        """Handle input."""
        if name in self._handlers:
            return self._handlers[name](**kwargs)
        return None


def prompt_yes_no(message: str, default: Optional[bool] = None) -> bool:
    """Prompt user for yes/no."""
    choices = "Y/n" if default is True else "y/N" if default is False else "y/n"
    response = input(f"{message} ({choices}): ").strip().lower()

    if not response:
        return default if default is not None else False

    return response in ('y', 'yes')


def prompt_choice(message: str, choices: List[str], default: Optional[int] = None) -> str:
    """Prompt user to choose from a list."""
    print(f"{message}")
    for i, choice in enumerate(choices):
        marker = "*" if default == i else " "
        print(f"  {marker} {i + 1}. {choice}")

    while True:
        try:
            response = input("Select: ").strip()
            if not response and default is not None:
                return choices[default]
            idx = int(response) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
        except ValueError:
            pass
        print("Invalid selection. Please try again.")


def prompt_text(message: str, default: str = "", required: bool = False) -> str:
    """Prompt user for text input."""
    prompt = f"{message}" + (f" [{default}]" if default else "") + ": "
    response = input(prompt).strip()

    if not response:
        if required:
            print("This field is required.")
            return prompt_text(message, default, required)
        return default

    return response


# Global helper instance
_helper = InteractiveHelper()


def get_helper() -> InteractiveHelper:
    """Get interactive helper instance."""
    return _helper


__all__ = [
    'InteractiveHelper',
    'prompt_yes_no',
    'prompt_choice',
    'prompt_text',
    'get_helper',
]