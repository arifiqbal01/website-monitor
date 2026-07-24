from src.database.connection import get_connection
from src.domain.model import (
    Website,
    WebsiteFailure,
    WebsiteFailureTypes,
    WebsiteReport,
    WebStatus,
)
from .website_repository import WebsiteRepository


class ReportRepository:

    def __init__(self):
        self.website_repository = WebsiteRepository()

    def save(self, report: WebsiteReport) -> int:
        """
        Saves a generic monitoring report.

        Returns the monitor_result_id.
        """

        website_id = self.website_repository.get_or_create(
            report.website
        )

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO monitor_results(
                website_id,
                status,
                response_time,
                http_code,
                failure_type,
                failure_message
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                website_id,
                report.status.name,
                report.response_time,
                report.http_code,
                report.failure.type.name,
                report.failure.message,
            ),
        )

        connection.commit()

        monitor_result_id = cursor.lastrowid

        connection.close()

        return monitor_result_id

    def get_latest(
        self,
        website: Website,
    ) -> WebsiteReport | None:
        """
        Returns the most recent monitoring report for a website.
        Returns None if no report exists.
        """

        website_id = self.website_repository.get(website)

        if website_id is None:
            return None

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                status,
                response_time,
                http_code,
                failure_type,
                failure_message,
                timestamp
            FROM monitor_results
            WHERE website_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (website_id,),
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return WebsiteReport(
            website=website,
            status=WebStatus[row["status"]],
            response_time=row["response_time"],
            http_code=row["http_code"],
            failure=WebsiteFailure(
                type=WebsiteFailureTypes[row["failure_type"]],
                message=row["failure_message"],
            ),
            timestamp=row["timestamp"],
        )