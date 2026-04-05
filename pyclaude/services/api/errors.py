"""API error handling utilities."""
from typing import Optional, Dict, Any


API_ERROR_MESSAGE_PREFIX = 'API Error'


def starts_with_api_error_prefix(text: str) -> bool:
    """Check if text starts with API error prefix."""
    return (
        text.startswith(API_ERROR_MESSAGE_PREFIX) or
        text.startswith(f"Please run /login · {API_ERROR_MESSAGE_PREFIX}")
    )


class APIError(Exception):
    """Base API error class."""
    def __init__(
        self,
        message: str,
        status: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status = status
        self.response = response or {}


class APIConnectionError(APIError):
    """Connection error during API call."""
    pass


class APIConnectionTimeoutError(APIError):
    """Connection timeout error."""
    pass


class RateLimitError(APIError):
    """Rate limit exceeded error."""
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class AuthenticationError(APIError):
    """Authentication failed."""
    pass


__all__ = [
    'API_ERROR_MESSAGE_PREFIX',
    'starts_with_api_error_prefix',
    'APIError',
    'APIConnectionError',
    'APIConnectionTimeoutError',
    'RateLimitError',
    'AuthenticationError',
]