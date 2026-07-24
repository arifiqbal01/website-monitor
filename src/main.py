import asyncio

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


async def main():

    print("1. Bootstrap")
    websites, config, processor = bootstrap()

    print("2. Run monitor")
    reports = await run_monitor(
        config=config,
        websites=websites,
    )

    print("3. Process reports")
    await processor.process(reports)

    print("4. Finished")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()