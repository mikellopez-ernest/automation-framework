# API Design

> Status: Stable
>
> Last updated: 2026-07-13

---

# Overview

Automation Framework exposes browser automations through a REST HTTP API built with FastAPI.

Clients interact with business-oriented operations without requiring any knowledge of Playwright or the target web application.

The API is intentionally thin.

Its responsibilities are limited to:

- request validation
- authentication
- dependency injection
- orchestration
- response generation

Browser automation remains entirely inside the framework.

---

# Design Principles

The API has been designed following these principles:

- Stateless HTTP interface
- Business-oriented endpoints
- Strong typing
- Explicit validation
- Versioned API
- Predictable error responses
- No Playwright concepts exposed publicly

---

# Base URL

```
/
```

---

# API Versioning

Current version:

```
/api/v1
```

Future incompatible changes should introduce:

```
/api/v2
```

The current version should remain stable until a breaking change becomes necessary.

---

# Authentication

Authentication uses a static Bearer token.

```
Authorization: Bearer <API_TOKEN>
```

The token is configured through:

```
AUTOMATION_API_TOKEN
```

Requests without a valid token return:

```
401 Unauthorized
```

---

# Current Endpoints

## Root

```
GET /
```

Returns basic API information.

---

## Health Check

```
GET /health
```

Returns the application status.

Intended for:

- monitoring
- reverse proxies
- container orchestration

---

## Export Tracking Report

```
POST /api/v1/dinantia/tracking/export
```

Exports the detailed Dinantia tracking report.

### Request

```json
{
    "school_year": "2025-26"
}
```

### Response

```
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

The response body contains the generated Excel file.

---

# Request Validation

Requests are validated using Pydantic models.

Invalid requests return:

```
422 Unprocessable Entity
```

Validation occurs before any browser automation starts.

---

# Execution Flow

```
HTTP Request

↓

Authentication

↓

Request validation

↓

Automation lock

↓

Dependency injection

↓

Application service

↓

Portal

↓

Workflow

↓

Page Objects

↓

Playwright

↓

Dinantia
```

The browser layer is completely hidden from API consumers.

---

# Concurrency

Only one browser automation may execute at a time.

The API serializes requests using an application-wide lock.

If another automation is already running:

```
409 Conflict
```

is returned.

Current implementation guarantees serialization within a single API process.

Production deployments should use a single Uvicorn worker.

---

# Temporary Files

Generated reports are never stored permanently.

Each request creates a unique temporary directory.

Example:

```
automation-tracking-a82f7c1d/
    tracking-report.xlsx
```

After the HTTP response has been fully transmitted:

- the report is deleted
- the temporary directory is removed

No cleanup tasks are required.

---

# Error Model

Framework exceptions are translated into HTTP responses.

Example:

```json
{
    "error": {
        "code": "dinantia_export_failed",
        "message": "Dinantia could not generate the tracking report."
    }
}
```

Unexpected exceptions never expose internal implementation details.

---

# HTTP Status Codes

| Status | Meaning |
|---------|---------|
| 200 | Successful operation |
| 400 | Invalid framework request |
| 401 | Missing or invalid Bearer token |
| 409 | Another automation is currently running |
| 422 | Invalid request body |
| 500 | Internal automation error |
| 502 | Upstream automation failure |
| 503 | Browser, download or export unavailable |

---

# Dependency Injection

FastAPI dependencies provide:

- application settings
- application services
- authentication
- concurrency control

Routers never instantiate framework components directly.

---

# Service Layer

Routers delegate all business logic to application services.

Responsibilities include:

- browser lifecycle
- portal creation
- configuration
- automation orchestration

Routers remain transport-only.

---

# OpenAPI

The API automatically exposes:

```
/openapi.json
```

Interactive documentation is available at:

```
/docs
```

No manual API documentation is required.

---

# End-to-End Validation

The API has been successfully validated against a real Dinantia environment.

Validation covered:

- authentication
- browser startup
- session reuse
- report generation
- HTTP file download
- automatic cleanup

The generated Excel file was verified to be structurally valid.

---

# Future Evolution

Future endpoints should follow the same architecture:

```
Router

↓

Service

↓

Portal

↓

Workflow

↓

Playwright
```

Browser automation should never be exposed directly through the HTTP API.

Every new endpoint must reuse the existing infrastructure for:

- authentication
- dependency injection
- concurrency
- exception handling
- temporary file management