# API Design

> **Audience:** Developers
>
> **Status:** Draft
>
> **Last Updated:** 2026-07-12
>
> **Applies To:** HTTP API

---

## Purpose

This document defines the initial HTTP API exposed by the Automation Framework.

Its objective is to establish the public contract before implementing the FastAPI layer.

The API will allow external systems, primarily Google Apps Script, to execute Dinantia tracking automations without interacting directly with Playwright or the internal Python architecture.

---

## Scope

The first API version covers:

* Service health checks.
* Authentication of API clients.
* Dinantia tracking report export.
* File delivery.
* Error responses.
* Concurrency restrictions.

This document does not cover:

* Server installation.
* Docker deployment.
* Reverse proxy configuration.
* TLS certificates.
* Google Apps Script implementation.
* Background job infrastructure.

Those topics will be documented separately.

---

## Design Principles

The API follows these principles:

* Expose business operations, not browser actions.
* Keep Playwright completely internal.
* Reuse the existing public Python API.
* Return predictable JSON errors.
* Protect every automation endpoint.
* Avoid unnecessary complexity in the first version.
* Preserve compatibility with Google Apps Script.

---

## Architecture

```text
Google Apps Script
        │
        │ HTTPS
        ▼
FastAPI
        │
        ▼
DinantiaPortal
        │
        ▼
Workflows
        │
        ▼
Page Objects
        │
        ▼
Playwright
        │
        ▼
Dinantia
```

FastAPI acts only as a transport layer.

It must not contain browser selectors, navigation logic or Dinantia-specific implementation details.

---

## Base Path

All public API endpoints use the following prefix:

```text
/api/v1
```

Versioning is included from the beginning to allow future changes without breaking existing clients.

---

## Endpoints

### Health Check

```http
GET /health
```

This endpoint verifies that the HTTP service is running.

It does not launch a browser or connect to Dinantia.

#### Response

```json
{
  "status": "ok"
}
```

#### HTTP Status

```text
200 OK
```

This endpoint may remain unauthenticated so that monitoring systems can use it.

---

### Export Dinantia Tracking Report

```http
POST /api/v1/dinantia/tracking/export
```

Exports the detailed Dinantia tracking report for a selected school year.

This endpoint executes the existing `DinantiaPortal.export_tracking_report()` operation.

#### Authentication

Required.

#### Request Body

```json
{
  "school_year": "2025-26"
}
```

#### Field Validation

| Field         | Type   | Required | Description                                  |
| ------------- | ------ | :------: | -------------------------------------------- |
| `school_year` | string |    Yes   | School year exactly as displayed by Dinantia |

Whitespace is removed before validation.

Empty values are rejected.

#### Successful Response

The first implementation will return the generated file directly as an HTTP download.

Recommended response headers:

```http
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="tracking-report.xlsx"
```

The response body contains the file bytes.

#### HTTP Status

```text
200 OK
```

---

## File Delivery Strategy

The initial API returns the generated file directly.

This strategy is preferred because:

* Google Apps Script can receive binary HTTP responses.
* No temporary public file URLs are required.
* No additional storage service is needed.
* The implementation remains simple.
* Generated reports do not remain exposed after the request completes.

The file may exist temporarily in the configured download directory while the request is processed.

Future implementations may use temporary object storage if report size, concurrency or execution time requires it.

---

## API Authentication

Automation endpoints must never be publicly accessible without authentication.

The initial version uses a static bearer token.

Example:

```http
Authorization: Bearer <api-token>
```

The token is configured through the environment:

```dotenv
AUTOMATION_API_TOKEN=replace-with-a-secure-random-value
```

The token must not be:

* committed to Git;
* embedded directly in Google Apps Script source code;
* included in logs;
* returned in errors.

Google Apps Script should store the token using `PropertiesService`.

---

## Authentication Errors

Missing or invalid bearer tokens return:

```text
401 Unauthorized
```

Example response:

```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or missing API token."
  }
}
```

The response should include:

```http
WWW-Authenticate: Bearer
```

---

## Error Format

All API errors use a consistent JSON structure.

```json
{
  "error": {
    "code": "dinantia_export_failed",
    "message": "Dinantia could not generate the tracking report."
  }
}
```

The `code` field is intended for programmatic handling.

The `message` field is intended for logs and user-facing diagnostics.

Internal stack traces, selectors, credentials and Playwright implementation details must never be returned to clients.

---

## Exception Mapping

Framework exceptions are translated into HTTP responses.

| Framework exception     | HTTP status | Error code                       |
| ----------------------- | :---------: | -------------------------------- |
| `ValidationError`       |     400     | `validation_error`               |
| Invalid API token       |     401     | `unauthorized`                   |
| `AuthenticationError`   |     502     | `dinantia_authentication_failed` |
| `DinantiaTrackingError` |     502     | `dinantia_tracking_failed`       |
| `DinantiaExportError`   |     503     | `dinantia_export_failed`         |
| `DownloadError`         |     503     | `download_failed`                |
| `BrowserError`          |     503     | `browser_unavailable`            |
| `AutomationError`       |     500     | `automation_error`               |
| Unexpected exception    |     500     | `internal_server_error`          |

Dinantia authentication failures use `502 Bad Gateway` rather than `401 Unauthorized`.

A `401` response refers to authentication against our API. Dinantia is an upstream system, so failures communicating with it are gateway failures.

---

## Validation Errors

Malformed or invalid requests return:

```text
400 Bad Request
```

Example:

```json
{
  "error": {
    "code": "validation_error",
    "message": "school_year cannot be empty."
  }
}
```

Request validation should occur before launching Playwright.

---

## Concurrency

The initial version allows only one Dinantia browser automation at a time.

Reasons include:

* shared authenticated session state;
* browser resource consumption;
* non-deterministic behaviour under simultaneous exports;
* risk of duplicate actions against Dinantia.

A process-level lock will protect automation execution.

If another request is already running, the initial implementation should return:

```text
409 Conflict
```

Example:

```json
{
  "error": {
    "code": "automation_busy",
    "message": "Another Dinantia automation is currently running."
  }
}
```

This behaviour is preferable to allowing requests to wait indefinitely.

---

## Execution Model

The first version executes synchronously.

```text
Request
   │
   ▼
Acquire automation lock
   │
   ▼
Launch browser
   │
   ▼
Execute workflow
   │
   ▼
Return generated file
   │
   ▼
Release lock
```

The HTTP connection remains open until the report is generated or the operation fails.

This model is intentionally simple and appropriate for low request volume.

---

## Timeouts

The API must define a maximum operation duration.

The initial timeout should allow for:

* browser startup;
* session validation;
* Dinantia navigation;
* chart loading;
* export retries;
* file transfer.

A request that exceeds the maximum duration should fail with:

```text
504 Gateway Timeout
```

Example:

```json
{
  "error": {
    "code": "automation_timeout",
    "message": "The Dinantia automation exceeded the maximum execution time."
  }
}
```

Timeout values should be configurable rather than hard-coded in endpoint functions.

---

## Idempotency

Exporting a report is a read-only operation from the user's perspective.

Repeated requests may produce multiple files but should not modify Dinantia data.

Future API operations that create or modify incidents will require stricter idempotency rules.

Those operations may introduce an optional header such as:

```http
Idempotency-Key: <unique-value>
```

Idempotency is not required for the initial export endpoint.

---

## Logging

Each request should generate structured lifecycle logs.

Example:

```text
Tracking export requested: school_year=2025-26
Automation lock acquired
Dinantia workflow started
Report generated
HTTP response completed
Automation lock released
```

Logs must not include:

* API tokens;
* Dinantia passwords;
* session cookies;
* storage state contents;
* report contents.

A request identifier should be included in future versions to correlate API logs with automation logs.

---

## Security

The API should only be exposed through HTTPS in production.

Additional recommended controls include:

* firewall restrictions;
* reverse proxy rate limiting;
* strong bearer token generation;
* periodic token rotation;
* restricted filesystem permissions;
* non-root container execution;
* limited access to `.env`;
* limited access to Playwright storage state.

The API must assume that possession of the bearer token grants access to Dinantia automation capabilities.

---

## Google Apps Script Compatibility

Google Apps Script will call the endpoint through `UrlFetchApp`.

Conceptual request:

```javascript
const response = UrlFetchApp.fetch(apiUrl, {
  method: "post",
  contentType: "application/json",
  headers: {
    Authorization: `Bearer ${apiToken}`,
  },
  payload: JSON.stringify({
    school_year: "2025-26",
  }),
  muteHttpExceptions: true,
});
```

On success, the response blob can be saved to Google Drive.

The detailed GAS implementation will be documented in `gas-integration.md`.

---

## OpenAPI

FastAPI will generate an OpenAPI specification automatically.

The API implementation should include:

* endpoint summaries;
* request model descriptions;
* response descriptions;
* documented status codes;
* reusable error schemas.

Interactive API documentation should be enabled in development.

Production exposure of interactive documentation may be restricted later.

---

## Proposed Package Structure

```text
automation/
└── api/
    ├── __init__.py
    ├── app.py
    ├── dependencies.py
    ├── errors.py
    ├── security.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── errors.py
    │   └── tracking.py
    └── routes/
        ├── __init__.py
        ├── health.py
        └── dinantia_tracking.py
```

Responsibilities:

| Module            | Responsibility                         |
| ----------------- | -------------------------------------- |
| `app.py`          | FastAPI application creation           |
| `dependencies.py` | Shared dependencies and execution lock |
| `security.py`     | Bearer token validation                |
| `errors.py`       | Exception-to-HTTP translation          |
| `schemas/`        | Request and response models            |
| `routes/`         | HTTP endpoint definitions              |

---

## Public Python API Usage

The HTTP layer must use only the stable public Python API.

Expected imports:

```python
from automation.config import get_settings
from automation.core import BrowserManager
from automation.models import TrackingFilters
from automation.portals.dinantia import DinantiaPortal
```

The API layer must not import:

* Page Objects;
* internal workflows;
* selectors;
* Playwright locators.

This restriction preserves the architectural boundary defined in `architecture.md`.

---

## Initial Implementation Milestones

The API should be implemented incrementally.

### Milestone 1

```text
GET /health
```

No Playwright integration.

### Milestone 2

Bearer-token authentication.

### Milestone 3

Request and error schemas.

### Milestone 4

Dinantia export endpoint using `DinantiaPortal`.

### Milestone 5

Concurrency lock and timeout handling.

### Milestone 6

Google Apps Script integration test.

### Milestone 7

Docker and server deployment.

Each milestone should remain independently testable.

---

## Future Evolution

Potential future changes include:

* asynchronous job execution;
* job status endpoints;
* temporary download URLs;
* multiple Dinantia accounts;
* session isolation per account;
* API token rotation;
* audit logging;
* rate limiting;
* additional tracking operations;
* incident creation endpoints.

These features should not be introduced until required by actual usage.

---

## Related Documents

* `architecture.md`
* `development-guide.md`
* `authentication-and-sessions.md`
* `dinantia-tracking.md`
* `adding-a-new-automation.md`
* `testing-and-debugging.md`
* `decisions/0003-layered-architecture.md`
