from src.domain.model import WebsiteReport, WordpressReport
from src.repositories import (
    ReportRepository,
    WordpressRepository,
)


class PersistenceService:

    def __init__(self):
        self.report_repository = ReportRepository()
        self.wordpress_repository = WordpressRepository()

    def save(self, report: WebsiteReport):

        if isinstance(report, WordpressReport):
            self.wordpress_repository.save(report)
        else:
            self.report_repository.save(report)