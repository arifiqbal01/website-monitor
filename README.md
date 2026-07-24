# Website Monitor

A Python-based website monitoring system that checks website availability, response health, and semantic failures. The project began as a learning exercise to explore asynchronous programming, networking, clean architecture, and domain modeling while building a practical monitoring tool.

Rather than relying only on HTTP status codes, the monitor attempts to determine whether a website is actually functioning correctly by detecting common semantic failures such as suspended hosting, expired domains, and WordPress-specific issues.

The implementation was written manually as part of the learning process. AI was used to understand concepts, architecture, and design decisions—not to generate the application itself.

---

# Features

## Website Monitoring

- Monitor multiple HTTP/HTTPS websites
- Concurrent checks using `asyncio`
- Configurable request timeout
- Automatic retry with exponential backoff
- Measure response time
- Record HTTP status codes

## Status Classification

Each website is classified into one of four states:

- **UP**
- **DOWN**
- **DEGRADED**
- **UNKNOWN**

Unlike traditional uptime monitors, a website returning `200 OK` is not automatically considered healthy.

## Semantic Failure Detection

Detects pages that technically respond but are not functioning correctly, including:

- Expired domains
- Hosting suspended
- Placeholder pages
- Error pages returned with HTTP 200

These websites are reported as **DEGRADED** rather than **UP**.

## WordPress Monitoring

For WordPress websites the monitor performs additional health checks including:

- WordPress version detection
- REST API availability
- XML-RPC availability
- Login page accessibility
- Database error detection
- Maintenance mode detection

## Notifications

- Slack webhook notifications
- State-change notifications
- Initial failure notifications

## Reporting

After every monitoring run the project generates:

- Plain-text summary report
- WordPress diagnostic report

## Persistence

Monitoring history is stored in SQLite.

---

# Project Structure

```
src/
├── config/
│   ├── loader.py
│   └── __init__.py
│
├── database/
│
├── domain/
│   ├── model.py
│   └── exceptions.py
│
├── evaluators/
│
├── helpers/
│
├── notifications/
│
├── processors/
│
├── repositories/
│
├── services/
│   ├── observe_website.py
│   ├── observe_wordpress.py
│   ├── status_checker.py
│   └── summary_maker.py
│
├── run_monitor.py
└── main.py
```

---

# Architecture

```
Configuration
        │
        ▼
Load Websites
        │
        ▼
Website Observer
        │
        ▼
Website Report
        │
        ▼
WordPress Observer (optional)
        │
        ▼
WordPress Report
        │
        ▼
Result Processor
        ├─────────────┐
        ▼             ▼
SQLite          Notification Evaluator
                      │
                      ▼
                Slack Notification
```

The project separates domain logic from infrastructure so that networking, persistence, and notifications remain independent from business rules.

---

# Technologies

- Python 3.12+
- asyncio
- aiohttp
- SQLite
- dataclasses
- Enum
- GitHub Actions
- python-dotenv

---

# Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```text
SLACK_ENABLED=true
SLACK_WEBHOOK_URL=YOUR_WEBHOOK
```

Run:

```bash
python -m src.main
```

---

# GitHub Actions

The project is designed to run automatically using GitHub Actions.

The workflow:

- Installs dependencies
- Loads secrets
- Executes the monitor
- Exits after completion

The schedule can be configured using cron expressions, for example:

```yaml
schedule:
  - cron: "*/30 * * * *"
```

or

```yaml
schedule:
  - cron: "0 * * * *"
```

---

# Example Report

```text
Report Summary

Total: 7
UP: 6
DOWN: 0
DEGRADED: 1

DEGRADED
https://webartsy.nl

WordPress Reports

Website: https://webartsy.nl
Status: DEGRADED
HTTP Code: 200
WordPress Version: 6.8.2
REST API: Disabled
XML-RPC: Enabled
Login Page: Accessible
Database Error: No
Maintenance Mode: No
```

---

# Roadmap

Future improvements include:

- Email notifications
- Microsoft Teams notifications
- Discord notifications
- HTML dashboard
- Historical charts
- Response-time graphs
- Daily summary reports
- SSL certificate monitoring
- Domain expiration monitoring
- Docker deployment
- Unit and integration tests
- Plugin-based monitoring extensions

---

# Learning Goals

This project was built to explore:

- Asynchronous programming
- HTTP networking
- Failure classification
- Domain-driven design principles
- Separation of concerns
- Clean architecture
- Repository pattern
- Configuration management
- Event evaluation
- Background automation
- Incremental software design

The objective is not to compete with enterprise monitoring platforms, but to understand how a monitoring system can be designed, implemented, and extended using modern Python practices.