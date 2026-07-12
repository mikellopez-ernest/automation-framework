# Architecture

> **Audience:** Developers
>
> **Status:** Stable
>
> **Last Updated:** 2026-07-11
>
> **Applies To:** Entire project

---

# Purpose

This document describes the architectural principles of the Automation Framework.

Its objective is to explain how the project is organized, the responsibilities of each layer, and the dependency rules that keep the codebase maintainable as new automations are added.

This document intentionally focuses on architecture rather than implementation details.

---

# Scope

This document covers:

* Overall project architecture.
* Layer responsibilities.
* Dependency rules.
* Public API philosophy.
* Project organization.

This document does **not** describe:

* Individual automations.
* Playwright selectors.
* Browser interactions.
* Deployment.
* FastAPI implementation.

Those topics are documented separately.

---

# Architectural Principles

The project is built around a small set of architectural principles.

## Single Responsibility

Each layer has a single responsibility.

Responsibilities are never shared between layers.

For example:

* Browser management belongs to the Core layer.
* UI interactions belong to Page Objects.
* Business processes belong to Workflows.
* Public APIs belong to Portals.

---

## Separation of Concerns

Browser automation should remain isolated from business logic.

The application using the framework should never interact directly with Playwright.

Instead, it should consume high-level operations.

Example:

```python
report = portal.export_tracking_report(filters)
```

instead of

```python
page.click(...)
page.fill(...)
page.wait_for(...)
```

---

## Reusable Infrastructure

Infrastructure that could be useful for another portal belongs to the Core layer.

Examples include:

* Browser lifecycle.
* Download management.
* Logging.
* Configuration.
* Common browser elements.

Infrastructure should never depend on portal-specific code.

---

## Explicit Domain Models

Business parameters should be grouped into typed models whenever possible.

Example:

```python
TrackingFilters(
    school_year="2025-26",
)
```

instead of passing multiple unrelated arguments.

Domain models make workflows easier to extend without breaking public APIs.

---

# Architecture Overview

The project follows a layered architecture.

```text
Applications
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
Core Infrastructure
        │
        ▼
Playwright
```

Dependencies always flow downwards.

Lower layers never depend on upper layers.

---

# Layer Responsibilities

## Applications

Applications are external consumers of the framework.

Examples include:

* Example scripts.
* FastAPI.
* Google Apps Script integrations.
* Scheduled tasks.

Applications only interact with Portal classes.

---

## Portals

Portals expose the public API of a supported web application.

A portal hides the internal implementation and offers business-oriented operations.

Example:

```python
portal.export_tracking_report(filters)
```

A Portal should never expose browser interactions.

---

## Workflows

Workflows coordinate multiple Page Objects to complete a business task.

Typical responsibilities include:

* Opening pages.
* Executing multiple navigation steps.
* Handling retries.
* Returning business results.

A Workflow should not contain reusable browser infrastructure.

---

## Page Objects

A Page Object represents a single application screen.

Its responsibility is to expose operations available within that screen.

Examples:

* Open a section.
* Fill a form.
* Click a button.
* Read displayed information.

Page Objects should never orchestrate complete business processes involving multiple screens.

---

## Core Infrastructure

The Core layer contains reusable components shared by every automation.

Current examples include:

* BrowserManager
* DownloadManager
* Elements
* Configuration
* Logging

The Core layer must remain completely independent from portal implementations.

---

## Playwright

Playwright is treated as an implementation detail.

Only the framework interacts directly with Playwright.

Applications should never depend on Playwright APIs.

---

# Dependency Rules

The dependency graph is intentionally simple.

```text
Applications
    ↓

Portals
    ↓

Workflows
    ↓

Page Objects
    ↓

Core
    ↓

Playwright
```

Allowed dependencies:

* Applications → Portals
* Portals → Workflows
* Workflows → Page Objects
* Page Objects → Core
* Core → Playwright

Forbidden dependencies include:

* Core → Portals
* Core → Workflows
* Page Objects → Workflows
* Workflows → Applications

Circular dependencies should never exist.

---

# Project Structure

```text
automation/
├── config/
├── core/
├── models/
├── portals/
├── workflows/
├── api/          (planned)
├── examples/
├── tests/
└── docs/
```

Each directory has a clearly defined responsibility.

When introducing new functionality, it should be placed in the layer that naturally owns that responsibility.

---

# Public API Philosophy

The framework exposes business operations rather than browser interactions.

Example:

```python
portal.export_tracking_report(filters)
```

The caller should never need to know:

* which pages are visited;
* how authentication works;
* how downloads are managed;
* how retries are implemented;
* which selectors are used.

Implementation details remain internal to the framework.

---

# Error Handling

Errors should be reported at the highest meaningful abstraction level.

Example:

Instead of exposing a Playwright timeout, the framework should raise an exception that describes the failed business operation.

```
Dinantia tracking report could not be exported.
```

rather than

```
Locator.wait_for() timed out.
```

Implementation-specific exceptions should remain internal whenever possible.

---

# Future Evolution

The architecture has been designed to support future additions without major structural changes.

Expected future components include:

* FastAPI service layer.
* Additional Dinantia tracking automations.
* Richer domain models.
* Improved automated testing.
* Additional reusable Core infrastructure.

These additions should integrate naturally without modifying the existing layering principles.

---

# Related Documents

* README.md
* development-guide.md
* authentication-and-sessions.md
* adding-a-new-automation.md
* ADR-0003 (Page / Workflow / Portal layering)
