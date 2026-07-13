# Architecture

> Status: Stable
>
> Last updated: 2026-07-13

---

# Overview

Automation Framework follows a layered architecture designed to isolate browser automation from business logic and HTTP transport.

Each layer has a single responsibility and communicates only with adjacent layers.

This architecture makes it possible to:

- add new automation providers without modifying the framework;
- expose browser automations through multiple interfaces (HTTP, CLI, scheduled jobs, etc.);
- test each layer independently;
- minimise maintenance when target platforms evolve.

---

# Architecture Diagram

```text
                    Client
                       │
                       ▼
                FastAPI Application
                       │
                       ▼
                    Routers
                       │
                       ▼
                 Dependencies
                       │
                       ▼
                   Services
                       │
                       ▼
                    Portals
                       │
                       ▼
                   Workflows
                       │
                       ▼
                  Page Objects
                       │
                       ▼
              Core Infrastructure
                       │
                       ▼
                  Playwright
                       │
                       ▼
               External Platform
```

---

# Layer Responsibilities

## FastAPI Application

Creates the application and configures:

- routers
- exception handlers
- OpenAPI
- Swagger UI

It contains no business logic.

---

## Routers

Routers expose HTTP endpoints.

Responsibilities:

- request parsing
- response generation
- dependency injection
- HTTP status codes

Routers must never:

- create browsers
- use Playwright
- contain business logic
- contain selectors

---

## Dependencies

Dependencies provide reusable infrastructure.

Examples:

- Settings
- Authentication
- Services
- Automation lock

Dependencies should be stateless whenever possible.

---

## Services

Services orchestrate complete application operations.

Responsibilities include:

- browser lifecycle
- portal creation
- temporary download directories
- configuration
- application flow

Services do not contain Playwright selectors.

---

## Portals

A Portal exposes a high-level API for a single external platform.

Example:

```python
portal.export_tracking_report(...)
```

Consumers never interact directly with Workflows or Page Objects.

---

## Workflows

A Workflow coordinates multiple Page Objects to perform a business operation.

Example:

```
Login

↓

Tracking

↓

Detail

↓

Export
```

Workflows own navigation logic.

---

## Page Objects

Page Objects represent individual screens.

Responsibilities:

- selectors
- clicks
- form filling
- waiting
- reading page data

Playwright interactions belong exclusively here.

---

## Core Infrastructure

Reusable infrastructure shared by every automation.

Examples:

- BrowserManager
- DownloadManager
- logging
- configuration
- exception hierarchy

Core must remain provider-independent.

---

## Playwright

Playwright is treated as an implementation detail.

The rest of the framework communicates only through abstractions.

---

# Dependency Direction

Dependencies always point downwards.

```text
Router
    ↓
Service
    ↓
Portal
    ↓
Workflow
    ↓
Page Object
    ↓
Core
```

Lower layers never import upper layers.

Examples:

✅ Allowed

```
Service → Portal
```

```
Workflow → Page Object
```

```
Page Object → Core
```

❌ Forbidden

```
Page Object → Service
```

```
Portal → Router
```

```
Core → Workflow
```

---

# Browser Lifecycle

The browser lifecycle is owned by the Service layer.

```text
Request

↓

Create BrowserManager

↓

Execute automation

↓

Close browser

↓

Return response
```

Routers never interact with BrowserManager.

---

# Authentication

Two independent authentication mechanisms exist.

## API Authentication

Used by external clients.

```
Bearer Token
```

Configured through:

```
AUTOMATION_API_TOKEN
```

---

## Dinantia Authentication

Used internally by browser automation.

```
Username

↓

Password

↓

Persistent storage state
```

These mechanisms must remain independent.

---

# Concurrency

Automation execution is serialized.

Only one browser automation may execute simultaneously within a process.

The Automation Lock is acquired before any browser starts.

```
Request A

↓

Browser

↓

Finished

↓

Request B
```

Multiple Uvicorn workers are intentionally not supported.

---

# Temporary Downloads

Every request receives its own temporary directory.

Example:

```
automation-tracking-a82fd19/

    tracking-report.xlsx
```

Lifecycle:

```
Create directory

↓

Download report

↓

HTTP response

↓

Automatic cleanup
```

No permanent reports are stored.

---

# Exception Handling

Framework exceptions propagate through the Service layer.

FastAPI translates them into HTTP responses using global exception handlers.

Routers should not catch framework exceptions.

---

# Configuration

Configuration is centralized in `Settings`.

Framework components receive configuration through dependency injection.

Credentials, paths and runtime options must never be hardcoded.

---

# Design Rules

Every new feature should follow the same architecture.

```
Model

↓

Page Objects

↓

Workflow

↓

Portal

↓

Service

↓

Router
```

Infrastructure should be reused whenever possible.

New providers should implement only the provider-specific layers.

---

# Architectural Principles

The project follows these principles:

- Single Responsibility Principle
- Separation of Concerns
- Explicit Dependencies
- Strong Typing
- Composition over Inheritance
- Reusable Infrastructure

Every architectural decision should reinforce these principles.

---

# Related Documentation

- `api-design.md`
- `development-guide.md`
- `authentication-and-sessions.md`
- `adding-a-new-automation.md`
- `decisions/`