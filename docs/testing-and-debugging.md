# Testing and Debugging

> Status: Stable
>
> Last updated: 2026-07-13

---

# Overview

Automation Framework uses multiple levels of testing to validate the framework, API and browser automations.

Testing should progressively increase confidence before deploying changes into production.

The recommended validation order is:

```
Unit Tests

↓

API Tests

↓

Manual Validation

↓

End-to-End Validation
```

---

# Test Pyramid

The project follows a layered testing strategy.

## Unit Tests

Purpose:

Validate isolated functionality.

Examples:

- Settings
- Domain models
- Validation
- Utility functions

These tests should never launch a browser.

---

## API Tests

Purpose:

Validate the HTTP layer.

Examples:

- Request validation
- Authentication
- Dependency injection
- HTTP responses
- File downloads

API tests should replace application services using FastAPI dependency overrides.

Playwright should never run during API tests.

---

## End-to-End Tests

Purpose:

Validate the complete browser automation.

Example flow:

```
HTTP Request

↓

Authentication

↓

Browser

↓

Dinantia

↓

Excel

↓

HTTP Response

↓

Cleanup
```

These tests execute the real automation.

---

# Running the Test Suite

Run every test.

```bash
uv run pytest
```

---

Run a single file.

```bash
uv run pytest tests/api/test_dinantia_tracking_routes.py
```

---

Run a single test.

```bash
uv run pytest -k export_tracking_report
```

---

# Static Analysis

Before committing:

```bash
uv run ruff check . --fix

uv run ruff format .

uv run ruff check .

uv run mypy
```

The repository should remain completely green.

---

# Manual API Testing

Start the API.

```bash
uv run uvicorn automation.api.app:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

OpenAPI:

```
http://127.0.0.1:8000/openapi.json
```

---

# Testing with curl

Example request:

```bash
curl \
  -X POST \
  http://127.0.0.1:8000/api/v1/dinantia/tracking/export \
  -H "Authorization: Bearer <API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"school_year":"2025-26"}' \
  --output tracking-report.xlsx
```

---

# Validating the Download

Confirm the file exists.

```bash
ls -lh tracking-report.xlsx
```

Confirm it is an Excel workbook.

```bash
file tracking-report.xlsx
```

Validate the ZIP structure.

```bash
unzip -t tracking-report.xlsx
```

Expected output:

```
No errors detected in compressed data
```

---

# Authentication Tests

Missing token:

Expected:

```
401 Unauthorized
```

---

Invalid token:

Expected:

```
401 Unauthorized
```

---

Missing configuration:

Expected:

```
503 Service Unavailable
```

---

# Request Validation

Invalid request body:

```json
{
    "school_year": ""
}
```

Expected:

```
422 Unprocessable Entity
```

Validation should occur before any browser is launched.

---

# Concurrency

Only one automation may execute at a time.

When another request is already running:

Expected:

```
409 Conflict
```

The browser should not start.

---

# Temporary Downloads

Every request creates a temporary directory.

Example:

```
automation-tracking-8fd29ab3/
```

The directory should disappear automatically after the response has finished.

Verify:

```bash
find /tmp -maxdepth 1 -type d -name "automation-tracking-*"
```

No directories should remain.

---

# Browser Sessions

Persistent browser state is stored separately.

Example:

```
.playwright/auth/dinantia.json
```

Downloaded reports should never be stored permanently.

---

# Logging

Useful information includes:

- browser startup
- authentication
- page navigation
- retries
- downloads
- browser shutdown

Unexpected exceptions should include stack traces.

HTTP clients should never receive internal implementation details.

---

# Common Problems

## Browser does not start

Verify:

- Playwright installation
- browser binaries
- permissions

---

## Authentication fails

Verify:

- username
- password
- storage state

Delete the stored browser session if necessary and authenticate again.

---

## Download timeout

Possible causes:

- Dinantia temporary failure
- popup window
- network latency

DownloadManager automatically retries failed downloads.

---

## HTTP 401

Verify:

```
Authorization: Bearer <token>
```

Confirm:

```
AUTOMATION_API_TOKEN
```

---

## HTTP 409

Another automation is already running.

Wait until the previous request finishes.

---

## HTTP 503

Possible causes:

- browser unavailable
- download failure
- report generation failure
- API token not configured

Review the application logs.

---

# Successful Validation Checklist

Before releasing changes:

- Ruff passes.
- MyPy passes.
- Pytest passes.
- Swagger loads correctly.
- OpenAPI specification is generated.
- Authentication works.
- Browser automation succeeds.
- Excel download is valid.
- Temporary directories are removed.
- No unexpected warnings appear.

---

# Related Documentation

- development-guide.md
- api-design.md
- authentication-and-sessions.md
- project-status.md