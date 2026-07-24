from src.domain.model import WordpressReport
from src.database.connection import get_connection
from .report_repository import ReportRepository


class WordpressRepository:

    def __init__(self):
        self.report_repository = ReportRepository()

    def save(self, report: WordpressReport):

        monitor_result_id = self.report_repository.save(report)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO wordpress_results(
                monitor_result_id,
                wordpress_version,
                rest_api,
                xmlrpc,
                login_page,
                database_error,
                maintenance_mode
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                monitor_result_id,
                report.wordpress_version,
                report.rest_api,
                report.xmlrpc,
                report.login_page,
                report.database_error,
                report.maintenance_mode,
            ),
        )

        connection.commit()

        connection.close()

        return monitor_result_id