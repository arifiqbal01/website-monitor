# Website Monitor

<<<<<<< HEAD
A Python tool that monitors website availability, response health, and semantic failures (e.g. suspended hosting, expired domains), built as a learning project to practice domain modeling and async I/O, and extended gradually as new features are added.

This is not a polished product. It's a working system built to understand real concepts — async networking, failure classification, and separating domain logic from I/O, without relying on AI to write the code. AI was used to understand concepts, not to generate the implementation.

## What it does

- Checks a list of websites on a fixed interval
- Classifies each result into a status: **UP**, **DOWN**, **DEGRADED**, or **UNKNOWN**
- Detects not just outages, but *semantic* failures — pages that return HTTP 200 but contain signals like "domain has expired" or "hosting account suspended"
- Writes a plain-text summary report after each check cycle

## Example output
=======
A Python project for monitoring website availability, response health, and semantic failures (such as expired domains or suspended hosting).

The project was started as a learning exercise to explore asynchronous programming, networking, error handling, and clean application architecture while building a practical monitoring tool. The goal is to gradually evolve the project by implementing real-world monitoring features one step at a time.

AI was used to understand concepts and architecture throughout the learning process, while the implementation itself was written manually.

---

## Project Goals

This project was designed to explore several real-world software engineering concepts, including:

- HTTP networking
- Asynchronous programming
- Error handling
- Logging
- Configuration management
- Data recording
- Domain modeling
- Maintainable project structure
- Long-running automation

The intention is to build the system incrementally instead of implementing every feature at once.

---

## Current Features

- Monitor multiple HTTP/HTTPS websites
- Concurrent website checks using `asyncio` and `aiohttp`
- Measure response time
- Classify website status as:
  - UP
  - DOWN
  - DEGRADED
  - UNKNOWN
- Detect semantic failures such as:
  - Domain expired
  - Hosting suspended
  - Placeholder pages
- Generate summary reports after each monitoring cycle
- Configurable website list
- Typed failure classification using domain models

---

## Why "DEGRADED" Exists

Most uptime monitors rely only on HTTP status codes.

A website can return `200 OK` while displaying:

- Domain has expired
- Hosting account suspended
- Maintenance placeholder

Although the server is responding, the website is not functioning correctly.

Instead of reporting these cases as **UP**, this project classifies them as **DEGRADED**.

---

## Example Report

```text
Report Summary

Total: 4
UP: 1
DOWN: 1
DEGRADED: 2

UP
https://google.com

DOWN
http://httpstat.us/503

DEGRADED
https://arif-iqbal.com/main
http://www.webartsy.site/
```

---

## Project Structure

```
src/
├── domain/
│   ├── model.py
│   └── exceptions.py
│
├── services/
│   ├── observer.py
│   ├── status_checker.py
│   └── summary_maker.py
│
├── helpers/
│   ├── loader.py
│   ├── logger.py
│   ├── normalize_url.py
│   ├── retry.py
│   └── now.py
│
├── main.py
└── run_monitor.py
```

---

## Architecture

```
Configuration
        │
        ▼
Load Website List
        │
        ▼
Observer (Async HTTP Checks)
        │
        ▼
Status Checker
        │
        ▼
Summary Generator
        │
        ▼
Report Output
```

The observer performs network operations while the status checker remains pure business logic, making status classification deterministic and easy to extend.

---

## Technologies

- Python 3.11+
- asyncio
- aiohttp
- dataclasses
- Enum-based domain models

---

## Original Requirements

The project was initially planned with the following objectives:

### Website Monitoring

- Monitor one or more websites
- Measure response time
- Record HTTP status codes
- Detect UP and DOWN states

### Failure Handling

- Invalid domains
- DNS failures
- Connection failures
- SSL errors
- Timeouts
- Internet outages

### Data Recording

Persist monitoring data including:

- Timestamp
- URL
- Status
- HTTP status code
- Response time

### Logging

Maintain readable logs for:

- Successful checks
- Failures
- Exceptions

### Automation

- Run continuously
- Recover safely after restart
- Avoid hardcoded configuration

### Extensibility

The architecture should support future additions such as:

- Email alerts
- Telegram notifications
- Charts
- Daily summaries
- Cloud deployment

---

## Current Status

### Implemented

- Async website monitoring
- Response timing
- Status classification
- Semantic failure detection
- Configurable website list
- Summary reporting
- Domain-driven status models

### Planned

- Retry mechanism
- Persistent monitoring history
- Structured JSON reports
- HTML reports
- Continuous scheduling
- Alert integrations
- Automated tests
- Docker support

---

## Running

```bash
pip install -r requirements.txt
python -m src.main
```

---

## Learning Objective

Rather than building a production-ready uptime service immediately, this repository documents the process of learning networking, asynchronous programming, clean architecture, and maintainable Python application design through incremental development.
>>>>>>> 4ba7194 (update repo readme and repo structure)
