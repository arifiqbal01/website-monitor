from src.domain.model import Config, SlackConfig
from .loader import load_config

__all__ = [
    "Config",
    "SlackConfig",
    "load_config",
]