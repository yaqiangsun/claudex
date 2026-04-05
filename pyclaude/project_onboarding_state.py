"""Project onboarding state management."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class OnboardingState:
    """Project onboarding state."""
    project_path: str = ""
    project_type: Optional[str] = None
    is_onboarded: bool = False
    onboarding_step: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


# Global onboarding state
_onboarding = OnboardingState()


def get_onboarding_state() -> OnboardingState:
    """Get current onboarding state."""
    return _onboarding


def set_project_type(project_type: str) -> None:
    """Set project type."""
    _onboarding.project_type = project_type
    _onboarding.last_updated = datetime.now()


def complete_onboarding() -> None:
    """Mark onboarding as complete."""
    _onboarding.is_onboarded = True
    _onboarding.last_updated = datetime.now()


def reset_onboarding() -> None:
    """Reset onboarding state."""
    global _onboarding
    _onboarding = OnboardingState()


__all__ = [
    'OnboardingState',
    'get_onboarding_state',
    'set_project_type',
    'complete_onboarding',
    'reset_onboarding',
]