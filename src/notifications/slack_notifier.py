from src.domain.model import SlackConfig
from .slack_client import SlackClient
from .slack_formatter import SlackFormatter


class SlackNotifier:

    def __init__(self, config: SlackConfig):
        self.enabled = config.enabled
        self.client = (
            SlackClient(config.webhook_url)
            if config.webhook_url
            else None
        )

    async def send(self, events):

        if not self.enabled or self.client is None:
            return

        for event in events:
            payload = SlackFormatter.format(event)
            await self.client.send(payload)