"""Coordinator Mode."""


class CoordinatorMode:
    """Coordinator mode state."""

    def __init__(self):
        self.enabled = False

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False


__all__ = ['CoordinatorMode']