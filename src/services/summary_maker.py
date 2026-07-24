from src.helpers.logger import logger
from src.domain.model import (
    WebsiteReport,
    WordpressReport,
    WebStatus,
)


def summary_maker(reports):
    up_websites = []
    down_websites = []
    degraded_websites = []
    unknown_websites = []

    wordpress_reports = []

    web_count = 0
    up_count = 0
    down_count = 0
    degraded_count = 0
    unknown_count = 0

    for report in reports:
        try:
            if not isinstance(report, WebsiteReport):
                logger.warning(f"Skipping invalid report: {report}")
                continue

            web_count += 1

            if report.status == WebStatus.UP:
                up_count += 1
                up_websites.append(report.website.url)

            elif report.status == WebStatus.DOWN:
                down_count += 1
                down_websites.append(report.website.url)

            elif report.status == WebStatus.DEGRADED:
                degraded_count += 1
                degraded_websites.append(report.website.url)

            elif report.status == WebStatus.UNKNOWN:
                unknown_count += 1
                unknown_websites.append(report.website.url)

            if isinstance(report, WordpressReport):
                wordpress_reports.append(report)

        except AttributeError as e:
            logger.error(f"{report}: {e}")

    report_file = "./reports/report.txt"

    with open(report_file, "w") as file:
        file.write("Report Summary\n")
        file.write("----------------------\n\n")

        file.write(f"Total: {web_count}\n")
        file.write(f"UP: {up_count}\n")
        file.write(f"DOWN: {down_count}\n")
        file.write(f"DEGRADED: {degraded_count}\n")

        if unknown_count:
            file.write(f"UNKNOWN: {unknown_count}\n")

        file.write("\n")

        if up_websites:
            file.write("UP\n")
            for website in up_websites:
                file.write(f"- {website}\n")
            file.write("\n")

        if down_websites:
            file.write("DOWN\n")
            for website in down_websites:
                file.write(f"- {website}\n")
            file.write("\n")

        if degraded_websites:
            file.write("DEGRADED\n")
            for website in degraded_websites:
                file.write(f"- {website}\n")
            file.write("\n")

        if unknown_websites:
            file.write("UNKNOWN\n")
            for website in unknown_websites:
                file.write(f"- {website}\n")
            file.write("\n")

        if wordpress_reports:
            file.write("\nWordPress Reports\n")
            file.write("----------------------\n\n")

            for wp in wordpress_reports:
                file.write(f"Website: {wp.website.url}\n")
                file.write(f"Status: {wp.status.name}\n")
                file.write(f"HTTP Code: {wp.http_code}\n")
                file.write(
                    f"WordPress Version: {wp.wordpress_version or 'Unknown'}\n"
                )
                file.write(
                    f"REST API: {'Enabled' if wp.rest_api else 'Disabled'}\n"
                )
                file.write(
                    f"XML-RPC: {'Enabled' if wp.xmlrpc else 'Disabled'}\n"
                )
                file.write(
                    f"Login Page: {'Accessible' if wp.login_page else 'Unavailable'}\n"
                )
                file.write(
                    f"Database Error: {'Yes' if wp.database_error else 'No'}\n"
                )
                file.write(
                    f"Maintenance Mode: {'Yes' if wp.maintenance_mode else 'No'}\n"
                )
                file.write("\n")