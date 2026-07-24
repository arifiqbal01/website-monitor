from src.helpers.logger import logger
from src.domain.model import (
    WebStatus,
    CheckResult,
    WebsiteFailureTypes,
)


def status_checker(result: CheckResult) -> WebStatus:
    logger.info(f"Initializing status check for {result.website.url}")

    if (
        result.http_code is not None
        and 200 <= result.http_code < 400
        and result.failure.type == WebsiteFailureTypes.NONE
    ):
        logger.info(f"{result.website.url} status is {WebStatus.UP.name}")
        return WebStatus.UP

    elif result.failure.type in (
        WebsiteFailureTypes.SEMANTIC,
        WebsiteFailureTypes.HTTP,
    ):
        logger.info(f"{result.website.url} status is {WebStatus.DEGRADED.name}")
        return WebStatus.DEGRADED

    elif (
        result.failure.type != WebsiteFailureTypes.NONE
        and result.http_code is None
    ):
        logger.info(f"{result.website.url} status is {WebStatus.DOWN.name}")
        return WebStatus.DOWN

    logger.info(f"{result.website.url} status is {WebStatus.UNKNOWN.name}")
    return WebStatus.UNKNOWN