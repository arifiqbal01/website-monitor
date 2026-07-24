from dataclasses import dataclass


@dataclass(frozen=True)
class MonitorSettings:
    interval_minutes: int
    timeout_seconds: int
    retries: int


@dataclass(frozen=True)
class SlackSettings:
    enabled: bool
    webhook_url: str | None


@dataclass(frozen=True)
class Settings:
    monitor: MonitorSettings
    slack: SlackSettings