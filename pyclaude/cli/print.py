"""
Console output and printing utilities.
"""

import sys
from typing import Any


# ANSI color codes
class Colors:
    """ANSI color codes."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'


def _write(text: str, file=sys.stdout) -> None:
    """Write text to file."""
    file.write(text)
    file.flush()


def _colorize(text: str, color: str) -> str:
    """Add color to text."""
    return f"{color}{text}{Colors.RESET}"


def print(*args: Any, **kwargs: Any) -> None:
    """Print text to stdout."""
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    file = kwargs.get('file', sys.stdout)

    _write(sep.join(str(arg) for arg in args) + end, file)


def println(*args: Any, **kwargs: Any) -> None:
    """Print text with newline to stdout."""
    print(*args, sep=kwargs.get('sep', ' '), end='\n', **kwargs)


def print_error(*args: Any, **kwargs: Any) -> None:
    """Print error message to stderr."""
    sep = kwargs.get('sep', ' ')
    msg = sep.join(str(arg) for arg in args)
    colored = _colorize(f"Error: {msg}", Colors.RED)
    _write(colored + '\n', sys.stderr)


def print_warning(*args: Any, **kwargs: Any) -> None:
    """Print warning message to stdout."""
    sep = kwargs.get('sep', ' ')
    msg = sep.join(str(arg) for arg in args)
    colored = _colorize(f"Warning: {msg}", Colors.YELLOW)
    _write(colored + '\n', sys.stdout)


def print_success(*args: Any, **kwargs: Any) -> None:
    """Print success message to stdout."""
    sep = kwargs.get('sep', ' ')
    msg = sep.join(str(arg) for arg in args)
    colored = _colorize(msg, Colors.GREEN)
    _write(colored + '\n', sys.stdout)


def print_info(*args: Any, **kwargs: Any) -> None:
    """Print info message to stdout."""
    sep = kwargs.get('sep', ' ')
    msg = sep.join(str(arg) for arg in args)
    colored = _colorize(msg, Colors.CYAN)
    _write(colored + '\n', sys.stdout)


def print_dim(*args: Any, **kwargs: Any) -> None:
    """Print dimmed text to stdout."""
    sep = kwargs.get('sep', ' ')
    msg = sep.join(str(arg) for arg in args)
    colored = _colorize(msg, Colors.DIM)
    _write(colored + '\n', sys.stdout)


def print_bold(*args: Any, **kwargs: Any) -> None:
    """Print bold text to stdout."""
    sep = kwargs.get('sep', ' ')
    msg = sep.join(str(arg) for arg in args)
    colored = _colorize(msg, Colors.BOLD)
    _write(colored + '\n', sys.stdout)


def clear_line() -> None:
    """Clear the current line."""
    _write('\r\033[K')


def erase_lines(n: int) -> None:
    """Erase n lines."""
    if n > 0:
        _write('\033[2K' + '\n' * (n - 1) + '\r')


# Spinner for loading states
class Spinner:
    """Terminal spinner."""

    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    index = 0

    def __init__(self, message: str = ''):
        self.message = message
        self.running = False

    def start(self) -> None:
        """Start the spinner."""
        self.running = True
        self._render()

    def stop(self) -> None:
        """Stop the spinner."""
        self.running = False
        clear_line()

    def _render(self) -> None:
        """Render the spinner frame."""
        if not self.running:
            return
        frame = self.frames[self.index % len(self.frames)]
        text = f"{frame} {self.message}"
        _write(f"\r{text}")
        self.index += 1

    def next(self) -> None:
        """Advance to next frame."""
        self._render()


# Progress bar
class ProgressBar:
    """Simple progress bar."""

    def __init__(self, total: int = 100, width: int = 40):
        self.total = max(1, total)
        self.width = width
        self.current = 0

    def update(self, current: int) -> None:
        """Update progress bar."""
        self.current = min(current, self.total)
        self._render()

    def increment(self, n: int = 1) -> None:
        """Increment progress."""
        self.update(self.current + n)

    def _render(self) -> None:
        """Render the progress bar."""
        filled = int(self.width * self.current / self.total)
        bar = '█' * filled + '░' * (self.width - filled)
        percent = int(100 * self.current / self.total)
        text = f"[{bar}] {percent}%"
        _write(f"\r{text}")


# Rich-style table (simplified)
class Table:
    """Simple text table."""

    def __init__(self, *headers: str):
        self.headers = headers
        self.rows: list[list[str]] = []
        self.column_widths = [len(h) for h in headers]

    def add_row(self, *values: str) -> None:
        """Add a row to the table."""
        values_list = list(values)
        self.rows.append(values_list)
        # Update column widths
        for i, val in enumerate(values_list):
            if i < len(self.column_widths):
                self.column_widths[i] = max(self.column_widths[i], len(str(val)))

    def render(self) -> str:
        """Render the table as string."""
        lines = []

        # Header
        header_line = ' | '.join(
            h.ljust(w) for h, w in zip(self.headers, self.column_widths)
        )
        lines.append(header_line)
        lines.append('-' * len(header_line))

        # Rows
        for row in self.rows:
            row_line = ' | '.join(
                str(v).ljust(w) for v, w in zip(row, self.column_widths)
            )
            lines.append(row_line)

        return '\n'.join(lines)


# Export
__all__ = [
    'print',
    'println',
    'print_error',
    'print_warning',
    'print_success',
    'print_info',
    'print_dim',
    'print_bold',
    'clear_line',
    'erase_lines',
    'Spinner',
    'ProgressBar',
    'Table',
    'Colors',
]