import asyncio
import time

from dotenv import load_dotenv

from src.database import initialize_database
from src.helpers.loader import loader
from src.processors import ResultProcessor

from .run_monitor import run_monitor


def bootstrap():
    load_dotenv()

    initialize_database()

    websites, config = loader()

    processor = ResultProcessor(config)

    return websites, config, processor


async def main(
    config,
    websites,
    processor,
):

    reports = await run_monitor(
        config=config,
        websites=websites,
    )

    await processor.process(reports)


def run():

    websites, config, processor = bootstrap()

    cycle_count = 1

    while True:

        print(f"**************** Cycle: {cycle_count} *************")

        asyncio.run(
            main(
                config=config,
                websites=websites,
                processor=processor,
            )
        )

        cycle_count += 1

        time.sleep(config.interval_minutes * 60)


if __name__ == "__main__":
    run()