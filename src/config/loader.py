import json
import os

from dotenv import load_dotenv
from ..helpers.normalize_url import normalize_url
from ..helpers.logger import logger
from ..domain import model

load_dotenv()

CONFIG_PATH = "./config.json"


def load_config():
    try:
        logger.info("Initializing loader")

        with open(CONFIG_PATH, "r") as read_file:
            data = json.load(read_file)

        monitor = data.get("monitor", {})

        config = model.Config(
            interval_minutes=monitor.get("interval-minutes", 1),
            timeout_seconds=monitor.get("timeout-seconds", 3),
            retries=monitor.get("retries", 3),
            slack=model.SlackConfig(
                enabled=os.getenv("SLACK_ENABLED", "false").lower() == "true",
                webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
            ),
        )

        websites = []

        for website_data in data.get("websites", []):
            website = normalize_url(
                website_data["url"],
                model.WebsiteType(
                    website_data.get("type", "generic")
                ),
            )
            websites.append(website)

        return websites, config

    except FileNotFoundError:
        logger.exception(
            f"Configuration file '{CONFIG_PATH}' not found."
        )
        raise

    except json.JSONDecodeError:
        logger.exception(
            f"Invalid JSON in '{CONFIG_PATH}'."
        )
        raise