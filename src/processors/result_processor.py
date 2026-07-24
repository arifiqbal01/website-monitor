from src.config import Config
from src.domain.model import WordpressReport

from src.evaluators import NotificationEvaluator
from src.notifications import SlackNotifier

from src.repositories import (
    ReportRepository,
    WordpressRepository,
)

from src.services.summary_maker import summary_maker


class ResultProcessor:

    def __init__(self, config: Config):

        self.report_repository = ReportRepository()
        self.wordpress_repository = WordpressRepository()

        self.notification_evaluator = NotificationEvaluator()

        self.slack_notifier = SlackNotifier(
            config.slack
        )

    async def process(self, reports):

        for report in reports:

            # Get previous report
            previous = self.report_repository.get_latest(
                report.website
            )

            # Evaluate notifications
            events = self.notification_evaluator.evaluate(
                previous=previous,
                current=report,
            )

            # Save report
            if isinstance(report, WordpressReport):
                self.wordpress_repository.save(report)
            else:
                self.report_repository.save(report)

            # Send notifications
            await self.slack_notifier.send(events)

            for event in events:
                print(event.message)

        summary_maker(reports)

        # Future
        # await self.email_notifier.send(events)
        # self.metrics.publish(reports)