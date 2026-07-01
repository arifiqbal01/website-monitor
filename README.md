# Website Monitor

A Python tool that monitors website availability, response health, and semantic failures (e.g. suspended hosting, expired domains), built as a learning project to practice domain modeling and async I/O, and extended gradually as new features are added.

This is not a polished product. It's a working system built to understand real concepts — async networking, failure classification, and separating domain logic from I/O, without relying on AI to write the code. AI was used to understand concepts, not to generate the implementation.

## What it does

- Checks a list of websites on a fixed interval
- Classifies each result into a status: **UP**, **DOWN**, **DEGRADED**, or **UNKNOWN**
- Detects not just outages, but *semantic* failures — pages that return HTTP 200 but contain signals like "domain has expired" or "hosting account suspended"
- Writes a plain-text summary report after each check cycle

## Example output
