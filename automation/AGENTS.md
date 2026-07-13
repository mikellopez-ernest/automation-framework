# AGENTS.md

# Automation Framework

Agent Instructions

Last Updated: 2026-07-13

---

# Purpose

This document defines the engineering principles that every AI agent and human contributor must follow when modifying this repository.

It is intentionally technology-agnostic.

The goal is to preserve the architecture, quality and long-term maintainability of the project.

Whenever this document conflicts with ad-hoc implementation shortcuts, this document takes precedence.

---

# Project Philosophy

Automation Framework is not a collection of Playwright scripts.

It is a reusable browser automation platform.

Browser automation is an implementation detail.

The public API of the framework consists of business operations.

Every design decision should reinforce this separation.

---

# Primary Objectives

Always prioritize, in this order:

1. Correctness
2. Maintainability
3. Readability
4. Simplicity
5. Performance

Never sacrifice architecture for minor performance gains.

---

# Core Principles

## Single Responsibility

Every component should have one clearly defined responsibility.

If a class starts solving multiple problems, split it.

---

## Layer Separation

Respect the architecture.

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

↓

Playwright
```

Dependencies always point downward.

Never introduce upward dependencies.

---

## Infrastructure First

Whenever a problem may appear in multiple automations, solve it in Core.

Do not duplicate infrastructure.

Examples:

- browser lifecycle
- downloads
- logging
- retry logic
- configuration
- exception handling

---

## Provider Isolation

Provider-specific code belongs only inside provider modules.

The Core layer must never know anything about:

- Dinantia
- Moodle
- Untis
- Microsoft 365

or any future provider.

---

## Business-Oriented API

The public API should expose business operations.

Good:

```
export_tracking_report()
```

Bad:

```
click_export_button()
```

HTTP endpoints should represent business actions.

---

# Playwright

Playwright is an implementation detail.

Only the following layers may directly use Playwright:

- Core
- Page Objects

Never expose:

- Locator
- Page
- Browser
- Selector

outside those layers.

---

# Services

Services own:

- browser lifecycle
- orchestration
- temporary resources
- application flow

Services do not contain selectors.

Services do not implement HTTP.

---

# Routers

Routers should remain extremely small.

Responsibilities:

- request validation
- dependency injection
- HTTP responses

Nothing else.

Business logic belongs elsewhere.

---

# Error Handling

Raise framework exceptions.

Allow global exception handlers to translate them into HTTP responses.

Do not catch exceptions unless there is a clear recovery strategy.

---

# Temporary Files

Generated files are request-scoped.

Never leave generated files permanently on disk.

Automatic cleanup should remain the default behaviour.

---

# Browser Sessions

Browser instances are ephemeral.

Authentication state is persistent.

Do not persist browser instances.

---

# Concurrency

Only one browser automation executes at a time.

Do not bypass the Automation Lock.

Future scalability should be achieved through a different architecture, not by weakening the existing guarantees.

---

# Documentation

Documentation is part of the codebase.

Any architectural change should update:

- documentation
- ADRs
- public API documentation

Code and documentation should evolve together.

---

# Testing

Every feature should include appropriate tests.

Prefer testing behaviour instead of implementation.

API tests should replace Services using dependency overrides.

Do not launch Playwright during router tests.

---

# Code Style

Prefer:

- explicit code
- descriptive names
- small functions
- strong typing

Avoid:

- clever code
- hidden side effects
- unnecessary abstractions

Readability is more important than reducing the number of lines.

---

# Dependencies

Before adding a dependency, ask:

1. Can the standard library solve this?
2. Can existing infrastructure solve this?
3. Is the dependency actively maintained?
4. Does it improve the project significantly?

Minimize external dependencies.

---

# Backwards Compatibility

Public APIs should remain stable whenever possible.

Breaking changes require:

- documentation updates
- roadmap updates
- versioning considerations

---

# Commits

Each commit should represent one logical change.

Good examples:

```
feat(api): add bearer authentication

fix(download): improve retry handling

docs: update architecture guide
```

Avoid combining unrelated changes.

---

# Decision Making

When multiple valid solutions exist, prefer the one that:

- simplifies the architecture;
- improves reuse;
- reduces maintenance;
- minimizes coupling;
- is easiest to understand six months later.

Optimize for future maintainers.

---

# Long-Term Vision

The framework should evolve into a reusable browser automation platform capable of integrating multiple providers through a consistent HTTP API.

The architecture should remain stable even as providers change.

Infrastructure should grow more slowly than functionality.

New automations should primarily add:

- Page Objects
- Workflows
- Portals

without requiring changes to the framework itself.

---

# What Should Rarely Change

The following are considered architectural foundations:

- layered architecture
- provider isolation
- reusable infrastructure
- business-oriented API
- strong typing
- documentation-first approach

Changing these principles requires a new ADR.

---

# Final Rule

When in doubt, choose the solution that makes the repository easier to understand for the next developer.

That developer may be another person, or another AI.