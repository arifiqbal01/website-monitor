import asyncio
from typing import Callable, TypeVar

from .logger import logger
from ..domain.exceptions import WebsiteError
from ..domain.model import WebsiteFailureTypes

T = TypeVar("T")


async def retry(
    operation: Callable[[], T],
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
) -> T:
    """
    Retry an async operation using exponential backoff.

    Retries only WebsiteError exceptions that are considered retryable.
    All other exceptions are raised immediately.
    """

    current_delay = delay

    for attempt in range(1, retries + 1):
        try:
            return await operation()

        except asyncio.CancelledError:
            raise

        except WebsiteError as e:
            logger.warning(
                f"Attempt {attempt}/{retries} failed: {e}"
            )

            # Semantic failures should never be retried
            if e.failure_type == WebsiteFailureTypes.SEMANTIC:
                logger.warning("Semantic failure detected. Not retrying.")
                raise

            if attempt == retries:
                logger.warning(
                    f"All {retries} retry attempts exhausted."
                )
                raise

            logger.info(
                f"Retrying in {current_delay} second(s)..."
            )

            await asyncio.sleep(current_delay)
            current_delay *= backoff

        except Exception:
            # Unexpected programming errors should not be retried.
            logger.exception("Unexpected error during retry operation.")
            raise