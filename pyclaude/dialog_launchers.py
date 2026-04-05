"""Dialog launchers for UI interactions."""
from typing import Optional, Dict, Any, Callable


class DialogLauncher:
    """Base class for dialog launchers."""

    def __init__(self):
        self._dialogs: Dict[str, Callable] = {}

    def register(self, name: str, handler: Callable) -> None:
        """Register a dialog handler."""
        self._dialogs[name] = handler

    def launch(self, name: str, **kwargs) -> Any:
        """Launch a dialog."""
        if name in self._dialogs:
            return self._dialogs[name](**kwargs)
        raise ValueError(f"Unknown dialog: {name}")

    def list_dialogs(self) -> list:
        """List available dialogs."""
        return list(self._dialogs.keys())


class ConfirmDialog(DialogLauncher):
    """Confirmation dialog."""

    def confirm(self, message: str, default: bool = False) -> bool:
        """Show confirmation dialog."""
        response = input(f"{message} (y/n): ").strip().lower()
        if not response:
            return default
        return response in ('y', 'yes')


class InputDialog(DialogLauncher):
    """Input dialog."""

    def get_input(self, message: str, default: str = "") -> str:
        """Get input from user."""
        if default:
            response = input(f"{message} [{default}]: ").strip()
            return response or default
        return input(f"{message}: ").strip()


# Global dialog launcher
_dialog_launcher = DialogLauncher()


def get_dialog_launcher() -> DialogLauncher:
    """Get global dialog launcher."""
    return _dialog_launcher


__all__ = [
    'DialogLauncher',
    'ConfirmDialog',
    'InputDialog',
    'get_dialog_launcher',
]