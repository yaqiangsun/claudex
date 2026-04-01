"""
API Key verification hook.

Python adaptation for verifying API keys.
"""

from enum import Enum
from typing import Optional, Callable


class VerificationStatus(str, Enum):
    """API key verification status."""
    LOADING = "loading"
    VALID = "valid"
    INVALID = "invalid"
    MISSING = "missing"
    ERROR = "error"


class ApiKeyVerificationResult:
    """Result of API key verification."""

    def __init__(
        self,
        status: VerificationStatus,
        reverify: Optional[Callable] = None,
        error: Optional[Exception] = None,
    ):
        self.status = status
        self.reverify = reverify
        self.error = error


# Cache for verification status
_cached_status: Optional[VerificationStatus] = None


def get_api_key_verification_status() -> VerificationStatus:
    """Get initial API key verification status."""
    global _cached_status

    if _cached_status is not None:
        return _cached_status

    # Check if we have auth enabled
    from ..utils.auth import is_anthropic_auth_enabled, is_claude_ai_subscriber

    if not is_anthropic_auth_enabled() or is_claude_ai_subscriber():
        _cached_status = VerificationStatus.VALID
        return _cached_status

    # Check if API key exists
    from ..utils.auth import get_anthropic_api_key_with_source

    key, source = get_anthropic_api_key_with_source()
    if key or source == "apiKeyHelper":
        _cached_status = VerificationStatus.LOADING
    else:
        _cached_status = VerificationStatus.MISSING

    return _cached_status


async def verify_api_key() -> ApiKeyVerificationResult:
    """Verify the API key."""
    global _cached_status

    from ..services.api.claude import verify_api_key as check_api_key
    from ..utils.auth import is_anthropic_auth_enabled, is_claude_ai_subscriber, get_anthropic_api_key_with_source

    if not is_anthropic_auth_enabled() or is_claude_ai_subscriber():
        _cached_status = VerificationStatus.VALID
        return ApiKeyVerificationResult(
            status=VerificationStatus.VALID,
            reverify=verify_api_key,
        )

    key, source = get_anthropic_api_key_with_source()
    if not key:
        if source == "apiKeyHelper":
            _cached_status = VerificationStatus.ERROR
            return ApiKeyVerificationResult(
                status=VerificationStatus.ERROR,
                error=Exception("API key helper did not return a valid key"),
                reverify=verify_api_key,
            )
        _cached_status = VerificationStatus.MISSING
        return ApiKeyVerificationResult(
            status=VerificationStatus.MISSING,
            reverify=verify_api_key,
        )

    try:
        is_valid = await check_api_key(key, verbose=False)
        status = VerificationStatus.VALID if is_valid else VerificationStatus.INVALID
        _cached_status = status
        return ApiKeyVerificationResult(
            status=status,
            reverify=verify_api_key,
        )
    except Exception as e:
        _cached_status = VerificationStatus.ERROR
        return ApiKeyVerificationResult(
            status=VerificationStatus.ERROR,
            error=e,
            reverify=verify_api_key,
        )


__all__ = [
    "VerificationStatus",
    "ApiKeyVerificationResult",
    "get_api_key_verification_status",
    "verify_api_key",
]