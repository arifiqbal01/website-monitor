import asyncio
import aiohttp

from src.helpers.logger import logger
from src.domain.model import (
    Config,
    Website,
    CheckResult,
    WebsiteFailure,
    WebsiteFailureTypes,
)
from src.domain.exceptions import (
    WebsiteError,
    SemanticError,
    HttpError,
    NetworkError,
    TimeoutError,
)


SUSPENDED_KEYWORDS = [
    "domain has been suspended",
    "account suspended",
    "hosting account suspended",
    "this account has been suspended",
    "contact your hosting provider",
    "payment overdue",
    "billing issue",
    "domain expired",
    "this domain has expired",
    "domain name has expired",
    "renew your domain",
    "domain is not configured",
    "no match for domain",
    "not found in registry",
    "this domain is parked",
]


async def observe_website(
    website: Website,
    config: Config,
) -> CheckResult:

    logger.info(f"Initializing HTTP request for {website.url}")

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=config.timeout_seconds)
        ) as session:

            async with session.get(website.url) as response:

                logger.info(f"Successful HTTP request for {website.url}")

                response_time = None
                http_code = response.status
                text = (await response.text()).lower()

                # aiohttp doesn't expose elapsed time like requests
                if hasattr(response, "elapsed"):
                    response_time = response.elapsed.total_seconds() * 1000

                for keyword in SUSPENDED_KEYWORDS:
                    if keyword in text and http_code == 200:
                        logger.warning(f"{website.url}: {keyword}")
                        raise SemanticError(keyword)

                if 400 <= http_code < 600:
                    logger.warning(f"HTTP {http_code} returned by {website.url}")
                    raise HttpError(http_code)

                return CheckResult(
                    website=website,
                    response_time=response_time,
                    http_code=http_code,
                    failure=WebsiteFailure(
                        WebsiteFailureTypes.NONE
                    ),
                )

    except aiohttp.ClientResponseError as e:
        logger.warning(f"HTTP request failed for {website.url}: {e}")
        raise HttpError(e.status)

    except aiohttp.ClientConnectorError as e:
        logger.warning(f"Network error for {website.url}: {e}")
        raise NetworkError()

    except asyncio.TimeoutError as e:
        logger.warning(f"Timeout for {website.url}: {e}")
        raise TimeoutError()

    except aiohttp.ClientError as e:
        logger.warning(f"Client error for {website.url}: {e}")
        raise WebsiteError()