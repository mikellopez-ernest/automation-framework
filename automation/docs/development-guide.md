# Development Guide

> **Audience:** Developers
>
> **Status:** Stable
>
> **Last Updated:** 2026-07-11
>
> **Applies To:** Entire project

---

# Purpose

This document describes the development workflow used throughout the project.

Its objective is to ensure that every new feature follows the same development process, coding standards, testing strategy and architectural principles.

---

# Scope

This document covers:

* Development environment.
* Project workflow.
* Coding conventions.
* Quality checks.
* Git workflow.
* General development practices.

This document does not describe individual automations or business workflows.

---

# Development Philosophy

The project follows a simple principle:

> Every change should improve the project without degrading its architecture.

New functionality is expected to integrate naturally into the existing layers instead of introducing shortcuts or duplicated logic.

---

# Development Environment

## Python

Python 3.11 or newer.

---

## Package Manager

The project uses **uv** for dependency management.

Install dependencies:

```bash
uv sync --dev
```

---

## Playwright

Install browser binaries:

```bash
uv run playwright install
```

---

## Environment Variables

Create the local configuration:

```bash
cp .env.example .env
```

Edit the `.env` file before executing examples.

Sensitive files must never be committed.

---

# Project Workflow

Every new feature follows the same workflow.

## 1. Understand the problem

Before writing code:

* understand the manual process;
* identify browser interactions;
* identify reusable behaviour;
* determine the architectural layer involved.

---

## 2. Design

Determine where the new functionality belongs.

Questions to ask:

* Is it reusable infrastructure?
* Is it specific to a page?
* Does it coordinate multiple pages?
* Is it part of the public API?

---

## 3. Implementation

Implement the smallest possible change.

Prefer several small commits over one large commit.

---

## 4. Testing

Execute the complete quality pipeline.

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
uv run mypy automation examples
uv run pytest
```

Whenever possible, execute the relevant example manually.

---

## 5. Documentation

Documentation is updated as part of the same feature.

Documentation is considered source code.

No feature is complete until its documentation has been updated.

---

## 6. Commit

Each commit should represent a single logical change.

Avoid mixing:

* refactoring;
* documentation;
* new functionality.

---

# Coding Standards

## Typing

Type annotations are required throughout the project.

Public functions should always be fully typed.

---

## Imports

Imports should remain organized according to Ruff.

Do not manually reorder imports.

Use:

```bash
uv run ruff check . --fix
```

---

## Formatting

Formatting is handled automatically.

```bash
uv run ruff format .
```

---

## Naming

Names should describe business concepts.

Examples:

* TrackingFilters
* DownloadManager
* BrowserManager

Avoid abbreviations whenever possible.

---

## Functions

Prefer small functions with a single responsibility.

Extract reusable behaviour instead of duplicating code.

---

## Classes

Classes should represent meaningful concepts.

Avoid utility classes that accumulate unrelated behaviour.

---

# Layer Responsibilities

Before introducing new code, determine its correct layer.

| Layer        | Responsibility                |
| ------------ | ----------------------------- |
| Core         | Shared infrastructure         |
| Models       | Business data                 |
| Page Objects | Single application screen     |
| Workflows    | Multi-page business processes |
| Portals      | Public API                    |

If uncertain, consult **architecture.md**.

---

# Testing Strategy

The project combines:

* Static analysis.
* Type checking.
* Unit tests.
* Manual verification.

All four are considered part of the development process.

---

# Git Workflow

Commits follow the Conventional Commits specification.

Examples:

```text
feat(dinantia): export tracking report

refactor(core): simplify download handling

docs: update architecture guide

test: add tracking filters tests
```

Keep commits focused.

---

# Documentation Workflow

Documentation evolves together with the implementation.

The preferred sequence is:

```text
Implementation
        ↓
Tests
        ↓
Documentation
        ↓
Commit
```

Documentation should never be postponed.

---

# Common Principles

Prefer:

* composition over duplication;
* explicit models over multiple primitive parameters;
* reusable infrastructure over portal-specific utilities;
* business-oriented APIs over browser interactions.

---

# Related Documents

* README.md
* architecture.md
* documentation-style-guide.md
* adding-a-new-automation.md
* testing-and-debugging.md
