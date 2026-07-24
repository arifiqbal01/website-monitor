Website Monitoring System - Developer Handover
Project Overview

This project has evolved from a simple website status checker into an extensible monitoring platform with a layered architecture.

Current goals:

Generic website health monitoring
Platform-specific observers (WordPress implemented)
Persistent monitoring history (SQLite)
Notification system (Slack in progress)
Future support for Shopify, Next.js, Laravel, FastAPI, SSL, WHOIS, etc.
Current Architecture
src/

├── config/
│
├── database/
│   ├── connection.py
│   ├── schema.py
│   └── database.db
│
├── domain/
│
├── evaluators/
│
├── notifications/
│
├── observers/
│   ├── generic/
│   └── wordpress/
│
├── processors/
│
├── repositories/
│
├── services/
│
└── main.py
Monitoring Flow

Current execution flow is designed as:

run_monitor()

        │

        ▼

Generic Observer

        │

        ▼

WebsiteReport

        │

        ▼

WordPress Observer (optional)

        │

        ▼

WordpressReport

        │

        ▼

ResultProcessor

        │
        ├── NotificationEvaluator
        │
        ├── SQLite Persistence
        │
        ├── SlackNotifier
        │
        └── Summary
Generic Observer

Already implemented.

Responsibilities:

HTTP request
Timeout detection
DNS failure
Network failure
HTTP error classification
Semantic keyword detection
Response time
Returns CheckResult

No platform-specific logic belongs here.

Platform Observers

Current:

WordpressObserver

Checks:

REST API
Login page
XMLRPC
Database connection errors
Maintenance mode

Returns:

WordpressReport

Future observers:

ShopifyObserver
LaravelObserver
NextJsObserver
FastApiObserver
Domain Models

Current models:

Website
WebsiteReport
WordpressReport

WebsiteFailure
WebsiteFailureTypes

Config

CheckResult
Required Improvements

Current:

status: str

Should become

status: WebStatus

Current

response_time: Optional[int]

Should become

response_time: float | None

Current

timestamp: datetime.now

Should become

timestamp: datetime
SQLite

Persistence is working.

Database:

database.db

Tables:

websites

monitor_results

wordpress_results

Verified working.

Example:

SELECT * FROM websites;

returns

google
github
openai
webartsy

Repository Layer

Current:

WebsiteRepository

ReportRepository

WordpressRepository

WebsiteRepository now has

get()

get_or_create()

Read/write responsibilities are separated.

ReportRepository

Now supports

save()

get_latest()

This is used for notification evaluation.

Result Processor

Current responsibility

for each report

    previous = repository.get_latest()

    events = evaluator.evaluate()

    save()

    slack()

summary()

Correct order is important.

Never save first.

Otherwise previous == current.

Notification System

Current structure

notifications/

    slack_client.py

    slack_formatter.py

    slack_notifier.py

Responsibilities

SlackClient

Only performs HTTP POST.

SlackFormatter

Converts NotificationEvent

↓

Slack JSON payload

SlackNotifier

Coordinates formatter + client.

Evaluator

Current

NotificationEvaluator

Returns

list[NotificationEvent]

Never sends Slack.

Never accesses HTTP.

Only decides

"What happened?"

Current notification rules

Website

UP

↓

DOWN

↓

WebsiteDownEvent

DOWN

↓

UP

↓

RecoveredEvent

UP

↓

DEGRADED

↓

DegradedEvent

WordPress

Database error

Maintenance mode

REST API unavailable

Future rules

Response time

SSL expiry

WHOIS expiry

Consecutive failures

Slack

Slack App created.

Incoming webhook configured.

Environment variable added.

SLACK_WEBHOOK_URL

Need to complete integration.

Slack payloads already designed.

Config

There was discussion about creating a second Settings object.

Decision:

Don't.

Use one Config.

Extend Config.

Example

@dataclass
class SlackConfig:

    enabled: bool

    webhook_url: str | None

Then

Config

interval

timeout

retries

slack

Single configuration object is preferred.

Current Problems

Several compile/runtime issues remain because refactoring is incomplete.

Examples encountered:

Settings vs Config

Solution

Use Config only.

WebsiteStatus

vs

WebStatus

Need consistent naming.

status

stored as string

Should become

WebStatus

Need to clean imports after Config refactor.

Slack Flow

Desired architecture

Evaluator

↓

Events

↓

Formatter

↓

Slack Client

↓

Slack

Slack should never know monitoring rules.

Future Components

Planned

EmailNotifier

TeamsNotifier

DiscordNotifier

WebhookNotifier

All consume

NotificationEvent
Notification Events

Current idea

WebsiteDownEvent

WebsiteRecoveredEvent

WebsiteDegradedEvent

WordpressDatabaseErrorEvent

RestApiUnavailableEvent

Future

SslExpiringEvent

DomainExpiringEvent

CertificateMismatchEvent
Database Future

Need historical queries

latest()

previous()

last_n()

failures()

uptime()

availability()

Used for

dashboards
uptime %
MTTR
MTBF
Summary Generator

Already works.

Supports

WebsiteReport

WordpressReport

Produces terminal summary.

Can later generate HTML or Markdown.

Recommended Next Tasks (Priority Order)
1. Finish Config refactor
Extend Config with SlackConfig.
Remove the separate Settings concept.
Update loader and ResultProcessor to use the unified Config.
2. Complete Slack integration
Finish SlackNotifier.
Verify webhook delivery with formatted payloads.
Replace debug print(event.message) with notifier calls.
3. Standardize domain models
Change WebsiteReport.status to WebStatus.
Change response_time to float | None.
Correct timestamp annotation to datetime.
Consider renaming WebStatus to WebsiteStatus for consistency if refactoring is acceptable.
4. Add richer notification rules

Implement:

Consecutive failures (e.g. notify after 3 failed checks)
Recovery messages including downtime
Response time degradation thresholds
WordPress REST API state changes (enabled/disabled)
Maintenance mode entry/exit
5. Improve persistence

Add repository methods such as:

get_previous()
get_recent(limit)
get_failures()
get_uptime_statistics()
6. Prepare for additional observers

The architecture is ready for:

Shopify
Next.js
Laravel
FastAPI
SSL certificate
Domain/WHOIS monitoring

Follow the same pattern used by WordpressObserver: keep the generic observer unchanged and layer platform-specific observers on top.

Overall Architecture Goal

The intended design is a modular monitoring framework where responsibilities are clearly separated:

Observers
      │
      ▼
Reports
      │
      ▼
ResultProcessor
      │
      ├── NotificationEvaluator
      │        │
      │        ▼
      │   Notification Events
      │        │
      ├────────┼─────────────┐
      ▼        ▼             ▼
 SQLite    SlackNotifier  Future Channels
      │
      ▼
Historical Analytics

The generic observer remains responsible only for connectivity and health checks. Platform observers add technology-specific insights. The evaluator decides whether an event is significant. Notification channels only deliver events, and repositories handle persistence. This separation keeps the system extensible as additional monitoring capabilities are added.