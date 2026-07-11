# Documentation Style Guide

## Purpose

This document defines the documentation standards used throughout the project.

Its goal is to ensure that every document follows the same structure, writing style, and level of detail, regardless of when it was written or who contributed to it.

Documentation is considered part of the project source code and should evolve together with the implementation.

---

# General Principles

Documentation should explain **why**, not only **how**.

The source code already explains the implementation. Documentation provides the context, design decisions, architecture and intended usage.

Whenever possible:

- Explain the motivation before the implementation.
- Prefer concepts over source code.
- Avoid duplicating information already present in the code.
- Keep documents concise.
- Keep documents updated.

If a document becomes outdated, it should be updated as part of the same change that modified the implementation.

---

# Writing Style

Documentation must be:

- Clear
- Concise
- Technical
- Objective
- Professional

Avoid:

- Marketing language
- Personal opinions
- Informal expressions
- Redundant explanations

Use present tense whenever possible.

Prefer active voice.

Example:

✔ The browser session is restored from the saved storage state.

instead of

✘ We try to restore the browser session.

---

# Language

All project documentation is written in English.

Code examples, diagrams and file names should also use English.

---

# Document Structure

Every document should follow this structure whenever applicable.

# Title

Short description of the document.

## Purpose

What this document explains.

## Scope

What is covered.

What is intentionally not covered.

## Concepts

High-level concepts required to understand the topic.

## Implementation

Description of the current implementation.

## Examples

Practical usage examples.

## Future Evolution

Possible future improvements.

## Related Documents

Links to related documentation.

Not every document needs every section, but the order should remain consistent.

---

# Document Metadata

Every document under the `docs/` directory must begin with the following metadata block.

> **Audience:** ...
>
> **Status:** Draft | Stable | Deprecated
>
> **Last Updated:** YYYY-MM-DD
>
> **Applies To:** ...

The project README is the only exception and should not include this metadata block.
# Diagrams

Simple ASCII diagrams are preferred over embedded images.

Example:

    Client
       │
       ▼
    FastAPI
       │
       ▼
    DinantiaPortal
       │
       ▼
    Workflow
       │
       ▼
    Page Objects
       │
       ▼
    Playwright

Diagrams should illustrate architecture, data flow or dependencies.

---

# Code Examples

Examples should be:

- Minimal
- Complete
- Copy-paste friendly

Only include the code necessary to explain the concept.

Avoid long listings.

---

# Folder Structure

When describing directories, use tree format.

Example:

automation/
├── config/
├── core/
├── models/
├── portals/
├── workflows/
└── api/

---

# Architecture Decisions

Large architectural decisions should not be explained repeatedly.

Instead, reference the corresponding ADR.

Example:

See ADR-0002 for the rationale behind persistent browser sessions.

---

# Cross References

Whenever another document explains a topic in more detail, reference it instead of duplicating the content.

Example:

See Architecture for more information about the project layers.

---

# Maintenance Rules

Documentation must be updated whenever:

- Public APIs change.
- Project structure changes.
- Design decisions change.
- Workflows change.
- New architectural concepts are introduced.

Documentation updates should be included in the same pull request or commit whenever possible.

---

# Versioning

Documentation follows the same versioning as the project.

There is no separate documentation release.

---

# Quality Checklist

Before committing documentation, verify that:

- The purpose is clearly stated.
- The scope is well defined.
- The document does not duplicate source code.
- Examples compile conceptually.
- Cross references are valid.
- Grammar and spelling have been reviewed.
- The document remains concise.