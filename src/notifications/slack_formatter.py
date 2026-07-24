from src.evaluators.notification_evaluator import NotificationEvent
from src.evaluators.rules import NotificationEventType


class SlackFormatter:

    @staticmethod
    def format(event: NotificationEvent) -> dict:

        color = SlackFormatter._color(event.event)

        return {
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": SlackFormatter._title(event),
                            },
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": (
                                        f"*Website*\n"
                                        f"{event.report.website.url}"
                                    ),
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": (
                                        f"*Status*\n"
                                        f"{event.report.status.name}"
                                    ),
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": (
                                        f"*HTTP*\n"
                                        f"{event.report.http_code or '-'}"
                                    ),
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": (
                                        f"*Failure*\n"
                                        f"{event.report.failure.type.name}"
                                    ),
                                },
                            ],
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": event.message,
                            },
                        },
                    ],
                }
            ]
        }

    @staticmethod
    def _title(event: NotificationEvent) -> str:

        titles = {
            NotificationEventType.WEBSITE_DOWN: "🔴 Website Down",
            NotificationEventType.WEBSITE_RECOVERED: "🟢 Website Recovered",
            NotificationEventType.WEBSITE_DEGRADED: "🟡 Website Degraded",
            NotificationEventType.WEBSITE_RESTORED: "🟢 Website Restored",
            NotificationEventType.WORDPRESS_DATABASE_ERROR: "🔴 WordPress Database Error",
            NotificationEventType.WORDPRESS_MAINTENANCE: "🟡 WordPress Maintenance Mode",
            NotificationEventType.WORDPRESS_REST_API_DOWN: "🟠 WordPress REST API Unavailable",
        }

        return titles.get(event.event, "Website Monitor")

    @staticmethod
    def _color(event_type: NotificationEventType) -> str:

        colors = {
            NotificationEventType.WEBSITE_DOWN: "#E01E5A",
            NotificationEventType.WEBSITE_RECOVERED: "#2EB67D",
            NotificationEventType.WEBSITE_DEGRADED: "#ECB22E",
            NotificationEventType.WEBSITE_RESTORED: "#2EB67D",
            NotificationEventType.WORDPRESS_DATABASE_ERROR: "#E01E5A",
            NotificationEventType.WORDPRESS_MAINTENANCE: "#ECB22E",
            NotificationEventType.WORDPRESS_REST_API_DOWN: "#ECB22E",
        }

        return colors.get(event_type, "#439FE0")