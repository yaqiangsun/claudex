"""REPL launcher for interactive sessions."""
import sys
from typing import Optional, Dict, Any


class REPLLauncher:
    """Launches and manages REPL sessions."""

    def __init__(self):
        self._running = False
        self._history = []

    def start(self) -> None:
        """Start REPL."""
        self._running = True
        print("Claude Code REPL started. Type /help for commands.")

    def stop(self) -> None:
        """Stop REPL."""
        self._running = False

    def is_running(self) -> bool:
        """Check if REPL is running."""
        return self._running

    def run_loop(self, prompt: str = "> ") -> None:
        """Run the REPL loop."""
        self.start()
        while self._running:
            try:
                user_input = input(prompt)
                if user_input.strip():
                    self._history.append(user_input)
                    self._process_input(user_input)
            except (KeyboardInterrupt, EOFError):
                self.stop()
                print("\nGoodbye!")

    def _process_input(self, input_str: str) -> None:
        """Process user input."""
        if input_str.strip() == "/exit":
            self.stop()
        # Process other commands here


def launch_repl() -> None:
    """Launch the REPL."""
    launcher = REPLLauncher()
    launcher.run_loop()


__all__ = ['REPLLauncher', 'launch_repl']