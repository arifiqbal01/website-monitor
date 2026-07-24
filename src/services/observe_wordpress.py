import aiohttp

from src.domain.model import (
    Config,
    WebsiteReport,
    WordpressReport,
)
from src.helpers.logger import logger


class WordpressObserver:

    async def observe(
        self,
        generic_result: WebsiteReport,
        config: Config,
    ) -> WordpressReport:

        website = generic_result.website

        logger.info(f"Initializing WordPress observer for {website.url}")

        wordpress_version = None
        rest_api = False
        xmlrpc = False
        login_page = False
        database_error = False
        maintenance_mode = False

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(
                total=config.timeout_seconds
            )
        ) as session:

            #
            # REST API
            #
            try:
                async with session.get(f"{website.url.rstrip('/')}/wp-json") as r:

                    if r.status == 200:
                        rest_api = True

                        data = await r.json(content_type=None)

                        wordpress_version = data.get("generator")

            except Exception as e:
                logger.warning(f"REST API check failed: {e}")

            #
            # Login page
            #
            try:
                async with session.get(
                    f"{website.url.rstrip('/')}/wp-login.php"
                ) as r:

                    login_page = r.status == 200

            except Exception as e:
                logger.warning(f"Login page check failed: {e}")

            #
            # XMLRPC
            #
            try:
                async with session.get(
                    f"{website.url.rstrip('/')}/xmlrpc.php"
                ) as r:

                    xmlrpc = r.status in (200, 405)

            except Exception as e:
                logger.warning(f"XML-RPC check failed: {e}")

            #
            # Homepage semantic checks
            #
            try:
                async with session.get(website.url) as r:

                    html = (await r.text()).lower()

                    database_error = (
                        "error establishing a database connection"
                        in html
                    )

                    maintenance_mode = (
                        "briefly unavailable for scheduled maintenance"
                        in html
                    )

            except Exception as e:
                logger.warning(f"Homepage check failed: {e}")

        return WordpressReport(
            website=generic_result.website,
            status=generic_result.status,
            response_time=generic_result.response_time,
            http_code=generic_result.http_code,
            failure=generic_result.failure,
            id=generic_result.id,
            timestamp=generic_result.timestamp,
            wordpress_version=wordpress_version,
            rest_api=rest_api,
            xmlrpc=xmlrpc,
            login_page=login_page,
            database_error=database_error,
            maintenance_mode=maintenance_mode,
        )