import aiohttp


class SlackClient:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send(self, payload: dict) -> None:

        async with aiohttp.ClientSession() as session:

            async with session.post(
                self.webhook_url,
                json=payload,
            ) as response:

                response.raise_for_status()