"""API retry logic with exponential backoff."""
import asyncio
import random
from typing import Any, Callable, Optional, TypeVar, AsyncGenerator

T = TypeVar('T')

DEFAULT_MAX_RETRIES = 10
BASE_DELAY_MS = 500
MAX_529_RETRIES = 3


class CannotRetryError(Exception):
    """Error when retries are exhausted."""
    def __init__(self, original_error: Any, retry_context: dict):
        self.original_error = original_error
        self.retry_context = retry_context
        super().__init__(str(original_error))


class FallbackTriggeredError(Exception):
    """Error when model fallback is triggered."""
    def __init__(self, original_model: str, fallback_model: str):
        self.original_model = original_model
        self.fallback_model = fallback_model
        super().__init__(f"Model fallback triggered: {original_model} -> {fallback_model}")


def is_529_error(error: Any) -> bool:
    """Check if error is a 529 (overloaded) error."""
    if not hasattr(error, 'status'):
        return False
    # Check status code or message content
    return (
        getattr(error, 'status', None) == 529 or
        ('message' in error and 'overloaded' in str(error.message).lower())
    )


def get_retry_after(error: Any) -> Optional[str]:
    """Extract retry-after header from error."""
    if hasattr(error, 'headers'):
        headers = error.headers
        if hasattr(headers, 'get'):
            return headers.get('retry-after')
        return headers.get('retry-after') if isinstance(headers, dict) else None
    return None


def get_retry_delay(
    attempt: int,
    retry_after_header: Optional[str] = None,
    max_delay_ms: int = 32000,
) -> float:
    """Calculate retry delay with exponential backoff and jitter."""
    if retry_after_header:
        try:
            seconds = int(retry_after_header)
            return seconds * 1000
        except ValueError:
            pass

    base_delay = min(BASE_DELAY_MS * (2 ** (attempt - 1)), max_delay_ms)
    jitter = random.random() * 0.25 * base_delay
    return base_delay + jitter


def should_retry(error: Any) -> bool:
    """Determine if an error should trigger a retry."""
    if not hasattr(error, 'status'):
        return False

    status = getattr(error, 'status', None)

    # Retry on connection errors
    if 'Connection' in type(error).__name__:
        return True

    if status is None:
        return False

    # Retry on request timeouts
    if status == 408:
        return True

    # Retry on lock timeouts
    if status == 409:
        return True

    # Retry on rate limits
    if status == 429:
        return True

    # Retry on auth errors
    if status == 401:
        return True

    # Retry on 529 (overloaded)
    if status == 529:
        return True

    # Retry on 5xx server errors
    if status >= 500:
        return True

    return False


async def with_retry(
    get_client: Callable,
    operation: Callable,
    max_retries: int = DEFAULT_MAX_RETRIES,
    signal: Optional[Any] = None,
) -> AsyncGenerator[dict, T]:
    """Execute operation with retry logic.

    Yields error messages and retries on transient failures.
    """
    last_error = None

    for attempt in range(1, max_retries + 2):
        if signal and getattr(signal, 'aborted', False):
            raise Exception("Request aborted")

        try:
            client = await get_client()
            result = await operation(client, attempt)
            return result
        except Exception as error:
            last_error = error

            if not should_retry(error):
                raise CannotRetryError(error, {'attempt': attempt}) from error

            if attempt > max_retries:
                raise CannotRetryError(error, {'attempt': attempt}) from error

            retry_after = get_retry_after(error)
            delay_ms = get_retry_delay(attempt, retry_after)

            yield {
                'type': 'retry',
                'error': str(error),
                'attempt': attempt,
                'max_retries': max_retries,
                'delay_ms': delay_ms,
            }

            await asyncio.sleep(delay_ms / 1000)

    raise CannotRetryError(last_error, {'attempt': attempt}) from last_error


__all__ = [
    'CannotRetryError',
    'FallbackTriggeredError',
    'is_529_error',
    'get_retry_delay',
    'should_retry',
    'with_retry',
    'DEFAULT_MAX_RETRIES',
    'BASE_DELAY_MS',
]