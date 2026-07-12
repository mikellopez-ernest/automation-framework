# Automation Framework

AI Development Guide

---

# Purpose

This document defines the engineering standards used throughout this repository.

Every contributor (human or AI) should read this file before modifying the project.

The objective is to keep the project consistent regardless of who produces the code.

---

# Project Philosophy

The project is built as a reusable automation framework.

It is NOT a collection of scripts.

Every design decision should favour:

- readability
- maintainability
- explicitness
- testability
- separation of concerns

Small improvements are preferred over large rewrites.

---

# Architecture

The architecture is intentionally layered.

```
HTTP API

↓

Router

↓

Service

↓

Portal

↓

Workflow

↓

Playwright

↓

External platform
```

Responsibilities must never leak between layers.

---

# Layer Responsibilities

## Router

Responsible only for HTTP.

Allowed:

- request parsing
- response generation
- dependency injection

Forbidden:

- Playwright
- selectors
- browser lifecycle
- business logic

---

## Service

Responsible for application orchestration.

Owns:

- BrowserManager
- Portal creation
- Settings
- application flow

Must not contain Playwright selectors.

---

## Portal

Represents a public automation API.

Owns:

- business operations

May use workflows.

Must never expose Playwright internals.

---

## Workflow

Coordinates several pages.

Owns navigation logic.

---

## Page Objects

Represent a single page.

Only here are Playwright locators allowed.

---

# Coding Standards

Python 3.11

Strict typing.

mypy must remain green.

ruff must remain green.

pytest must remain green.

No warnings should be introduced intentionally.

---

# Style

Prefer small functions.

Prefer explicit names.

Avoid abbreviations.

Avoid clever code.

Prefer readability over conciseness.

---

# Exceptions

Never raise RuntimeError directly.

Use framework exceptions.

New exceptions should inherit from AutomationError.

---

# Configuration

Never hardcode:

- credentials
- URLs
- tokens

Everything configurable belongs in Settings.

---

# Dependency Injection

FastAPI dependencies belong in:

automation/api/dependencies.py

Routers must use injected services.

---

# Testing

Every public feature should include tests.

Prefer isolated tests.

Mock services instead of browsers whenever possible.

---

# Documentation

Any significant architectural change must update:

- project-status.md

and, if necessary,

- roadmap.md

Architecture changes should also update the corresponding ADR.

---

# Commits

Each commit should represent one architectural decision.

Avoid mixing:

- refactoring
- documentation
- features
- bug fixes

Example:

GOOD

feat(api): add bearer authentication

BAD

update api

---

# Before Finishing Any Task

Run:

uv run ruff check . --fix

uv run ruff format .

uv run mypy

uv run pytest

The repository should remain green.

---

# Long-Term Goal

The framework should allow adding new automation providers without modifying the HTTP API architecture.

Dinantia is only the first implementation.