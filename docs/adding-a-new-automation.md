# Adding a New Automation

> Status: Stable
>
> Last updated: 2026-07-13

---

# Overview

This document describes the recommended process for adding a new browser automation to the framework.

The objective is to reuse the existing infrastructure whenever possible.

New automations should integrate naturally into the existing architecture without requiring framework modifications.

---

# Development Order

Every automation should be implemented in the following order.

```
Domain Model

↓

Page Objects

↓

Workflow

↓

Portal

↓

Application Service

↓

HTTP Router

↓

Tests

↓

Documentation
```

Skipping layers generally leads to duplicated code and poor separation of concerns.

---

# Step 1 — Create Domain Models

Create any models required to represent the automation.

Location:

```
automation/models/
```

Examples:

- request filters
- search criteria
- result models

Models should use Pydantic whenever validation is required.

---

# Step 2 — Create Page Objects

Represent each browser page independently.

Location:

```
automation/portals/<provider>/
```

Example:

```
login.py

home.py

tracking.py

detail.py
```

Responsibilities:

- selectors
- clicks
- waits
- reading page data

Page Objects should never coordinate complete business operations.

---

# Step 3 — Build the Workflow

Create a workflow that coordinates multiple pages.

Location:

```
automation/workflows/<provider>/
```

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

The workflow owns navigation logic.

---

# Step 4 — Extend the Portal

Expose the new functionality through the public portal API.

Example:

```python
portal.export_tracking_report(...)
```

The Portal should hide:

- Page Objects
- Workflows
- Playwright

Consumers interact exclusively with the Portal.

---

# Step 5 — Create an Application Service

If the automation should be exposed through HTTP, create a Service.

Responsibilities:

- browser lifecycle
- temporary downloads
- portal creation
- configuration
- orchestration

Services must not contain Playwright selectors.

---

# Step 6 — Expose an HTTP Endpoint

If the automation should be publicly available:

Create:

- request schema
- router
- dependency injection
- endpoint

The Router should only:

- validate requests
- invoke the Service
- return responses

No business logic belongs in the Router.

---

# Step 7 — Add Tests

Testing should cover multiple layers.

## Models

Validate input.

---

## Services

Validate orchestration.

---

## API

Validate:

- authentication
- request validation
- HTTP responses
- dependency injection

Replace Services with test doubles.

Do not launch Playwright.

---

## End-to-End

Validate the complete browser automation against the real platform.

---

# Step 8 — Update Documentation

Documentation should always evolve together with the code.

At minimum update:

- project-status.md
- roadmap.md (if applicable)
- provider documentation
- API documentation

If the architecture changes:

- update architecture.md
- create a new ADR

---

# Directory Layout

A typical implementation adds files similar to:

```
automation/

models/
    attendance.py

portals/provider/
    attendance.py

workflows/provider/
    attendance_export.py

api/
    schemas.py
    services.py
    routes/

tests/
    api/
```

Reuse existing infrastructure whenever possible.

---

# Existing Infrastructure

Before creating new components, verify whether the framework already provides:

- BrowserManager
- DownloadManager
- logging
- configuration
- exception handling
- authentication
- concurrency control
- temporary downloads

Duplicating infrastructure should be avoided.

---

# Architectural Rules

Every new automation should respect the existing dependency flow.

```
Router

↓

Service

↓

Portal

↓

Workflow

↓

Page Objects

↓

Core
```

Dependencies must never point upwards.

---

# Exception Handling

Raise framework exceptions.

Do not expose implementation-specific exceptions through the public API.

Global exception handlers translate framework exceptions into HTTP responses.

---

# Temporary Files

Generated files should:

- use request-scoped temporary directories;
- be removed automatically after the HTTP response;
- never remain permanently on disk.

---

# Checklist

Before considering a new automation complete:

- Domain models implemented.
- Page Objects implemented.
- Workflow implemented.
- Portal updated.
- Service created.
- Router created (if required).
- Tests passing.
- Documentation updated.
- Ruff passes.
- MyPy passes.
- Pytest passes.
- End-to-end validation completed.

---

# Related Documentation

- architecture.md
- api-design.md
- development-guide.md
- testing-and-debugging.md
- decisions/