from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import uuid
from datetime import datetime

class WebsiteType(str, Enum):
    GENERIC = "generic"
    WORDPRESS = "wordpress"
    SHOPIFY = "shopify"
    NEXTJS = "nextjs"
    LARAVEL = "laravel"
    FASTAPI = "fastapi"

@dataclass(frozen=True)
class Website:
    url: str
    type: WebsiteType = WebsiteType.GENERIC

from dataclasses import dataclass

@dataclass(frozen=True)
class SlackConfig:
    enabled: bool
    webhook_url: str | None = None

@dataclass(frozen=True)
class Config:
    interval_minutes: int
    timeout_seconds: int
    retries: int
    slack: SlackConfig

class WebsiteEvents(Enum):
    CHECK_STARTED = auto()
    CHECK_SUCCEEDED = auto()
    DNS_FAILURE = auto()
    TIMEOUT = auto()
    HTTP_ERROR = auto()
    RECOVERED = auto()

@dataclass
class WebsiteEvent:
    type: WebsiteEvents
    subject: str
    time: str
    source: str
    message: Optional[str] = None

class SystemEvents(Enum):
    CONFIG_LOADED = auto()
    CONFIG_FILE_MISSING = auto()
    INVALID_URL_IN_CONFIG = auto()
    JSON_PARSE_ERROR = auto()
    INTERNAL_ERROR = auto()

@dataclass
class SystemEvent:
    type: SystemEvents
    subject: str
    time: str
    source: str
    message: Optional[str] = None

class WebsiteFailureTypes(Enum):
    NONE = auto()
    DNS = auto()
    NETWORK = auto()
    TIMEOUT = auto()
    HTTP_SERVER = auto()
    HTTP_CLIENT = auto()
    HTTP_REDIRECT = auto()
    HTTP = auto()
    SEMANTIC = auto()
    INVALID_URL = auto()
    UNKNOWN = auto()

@dataclass
class WebsiteFailure:
    type: WebsiteFailureTypes
    message: Optional[str] = None

class SystemFailureTypes(Enum):
    NONE = auto()
    InvalidConfig = auto()
    InvalidURL = auto()
    ConfigNotFound = auto()
    ParseError = auto()
    InternalError = auto()
    Misconfiguration = auto()

@dataclass
class SystemFailure:
    type: SystemFailureTypes
    message: Optional[str] = None

@dataclass
class CheckResult:
    website: Website
    response_time: Optional[int]
    http_code: Optional[int]
    failure: WebsiteFailure


class WebStatus(Enum):
    UP = auto()
    DOWN = auto()
    DEGRADED = auto()
    UNKNOWN = auto()

@dataclass(frozen=True)
class WebsiteReport():
    website: Website
    status: WebStatus
    response_time: Optional[int]
    http_code: Optional[int]
    failure: WebsiteFailure
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime.now = field(default_factory=datetime.now)

@dataclass(frozen=True)
class WordpressReport(WebsiteReport):
    wordpress_version: str | None = None
    rest_api: bool = False
    xmlrpc: bool = False
    login_page: bool = False
    database_error: bool = False
    maintenance_mode: bool = False