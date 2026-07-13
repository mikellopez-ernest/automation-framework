# Development Guide

> Status: Stable
>
> Last updated: 2026-07-13

---

# Overview

This document describes the recommended development workflow for Automation Framework.

Following these guidelines helps keep the project consistent, maintainable and easy to extend.

---

# Development Philosophy

The framework follows a few simple rules.

- Make small, isolated changes.
- Keep every layer focused on a single responsibility.
- Prefer composition over inheritance.
- Prefer explicit code over clever code.
- Never sacrifice readability for brevity.
- Keep the repository green at all times.

Every commit should leave the project in a working state.

---

# Development Workflow

A typical feature should follow this order.

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

↓

Tests

↓

Documentation
```

Infrastructure should only be modified when it benefits multiple automations.

---

# Local Environment

## Install dependencies

```bash
uv sync --dev
```

---

## Install Playwright browsers

```bash
uv run playwright install
```

---

## Configure the environment

```bash
cp .env.example .env
```

Fill in the required configuration values.

---

# Running the API

Start the development server.

```bash
uv run uvicorn automation.api.app:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

OpenAPI:

```
http://127.0.0.1:8000/openapi.json
```

---

# Code Quality

Every change must pass the complete validation pipeline.

```bash
uv run ruff check . --fix

uv run ruff format .

uv run ruff check .

uv run mypy

uv run pytest
```

The repository should always remain green.

---

# Testing Strategy

Testing is divided into several layers.

## Unit Tests

Test isolated functionality.

Examples:

- models
- configuration
- utility functions

---

## API Tests

Use FastAPI's TestClient.

Application services should be replaced using dependency overrides.

Avoid launching Playwright during router tests.

---

## End-to-End Tests

End-to-end validation should be performed against a real Dinantia environment.

Typical validation includes:

- authentication
- browser startup
- report generation
- Excel download
- automatic cleanup

---

# Dependency Injection

Routers should never instantiate services directly.

Always obtain dependencies through FastAPI.

Example:

```python
service: TrackingServiceDependency
```

---

# Error Handling

Framework exceptions should propagate naturally.

Global exception handlers translate them into HTTP responses.

Routers should never catch framework exceptions.

---

# Browser Usage

BrowserManager belongs exclusively to the Service layer.

Do not instantiate BrowserManager from:

- routers
- portals
- workflows
- page objects

---

# Playwright

Playwright should only appear inside Page Objects and reusable infrastructure.

Selectors must never appear in:

- routers
- services
- portals

---

# Temporary Files

Generated reports should always use request-scoped temporary directories.

Never store exported files permanently.

Cleanup should happen automatically after the HTTP response has been sent.

---

# Adding a New Automation

The recommended order is:

1. Create typed models.
2. Implement Page Objects.
3. Build the Workflow.
4. Expose the Portal API.
5. Add the Service.
6. Create the Router.
7. Add automated tests.
8. Update the documentation.

---

# Debugging

Useful commands:

Run the API:

```bash
uv run uvicorn automation.api.app:app --reload
```

Run all tests:

```bash
uv run pytest
```

Run a single test:

```bash
uv run pytest tests/api/test_dinantia_tracking_routes.py
```

Type checking:

```bash
uv run mypy
```

Linting:

```bash
uv run ruff check .
```

Formatting:

```bash
uv run ruff format .
```

---

# Commit Guidelines

Each commit should represent one logical change.

Good examples:

```
feat(api): add bearer authentication

fix(download): improve retry handling

docs: update architecture guide
```

Avoid combining unrelated changes in a single commit.

---

# Pull Request Checklist

Before considering a feature complete:

- Architecture remains consistent.
- Documentation is updated.
- Ruff passes.
- MyPy passes.
- Pytest passes.
- End-to-end behaviour has been verified when applicable.
- No unnecessary dependencies have been introduced.

---

# Related Documentation

- README.md
- architecture.md
- api-design.md
- testing-and-debugging.md
- adding-a-new-automation.md