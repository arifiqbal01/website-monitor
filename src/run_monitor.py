import asyncio

from src.helpers.retry import retry
from src.services.observe_website import observe_website
from src.services.observe_wordpress import WordpressObserver
from src.services.status_checker import status_checker

from src.domain.model import (
    Config,
    Website,
    WebsiteFailure,
    WebsiteFailureTypes,
    CheckResult,
    WebsiteReport,
    WordpressReport,
    WebsiteType,      # Assuming you have this enum
)

from src.domain.exceptions import WebsiteError


async def run_monitor(config: Config, websites: list[Website]):
    tasks = []

    for website in websites:

        async def task(w=website):

            try:
                result = await retry(
                    lambda: observe_website(w, config),
                    retries=3,
                    delay=1,
                    backoff=2,
                )

            except WebsiteError as e:

                # TODO:
                # HttpError/SemanticError should ideally carry response_time
                # and http_code instead of referencing `result`.

                result = CheckResult(
                    website=w,
                    response_time=None,
                    http_code=None,
                    failure=WebsiteFailure(
                        type=e.failure_type,
                        message=str(e),
                    ),
                )

            status = status_checker(result)

            generic_report = WebsiteReport(
                website=w,
                status=status,
                response_time=result.response_time,
                http_code=result.http_code,
                failure=result.failure,
            )

            #
            # WordPress-specific checks
            #
            if (
                w.type == WebsiteType.WORDPRESS
                and result.failure.type == WebsiteFailureTypes.NONE
            ):
                observer = WordpressObserver()

                return await observer.observe(
                    generic_result=generic_report,
                    config=config,
                )

            return generic_report

        tasks.append(task())

    return await asyncio.gather(*tasks, return_exceptions=True)