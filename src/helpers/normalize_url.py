from urllib.parse import urlparse
import socket

from ..domain.model import Website, WebsiteType
from .logger import logger


def normalize_url(url: str, website_type: WebsiteType) -> Website:
    logger.info(f"Initializing normalization for {url}")

    parsed = urlparse(url)

    # Add https:// if missing
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    # Validate hostname
    socket.getaddrinfo(parsed.netloc, None)

    normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    logger.info(f"Normalization completed for {normalized_url}")

    return Website(
        url=normalized_url,
        type=website_type,
    )