# Adding a New Automation

> **Audience:** Developers
>
> **Status:** Stable
>
> **Last Updated:** 2026-07-11
>
> **Applies To:** Entire project

---

# Purpose

This document describes the recommended process for implementing a new browser automation within the Automation Framework.

Following these guidelines ensures that new functionality integrates naturally with the existing architecture while remaining maintainable and reusable.

---

# Scope

This document covers:

* Analysing a manual workflow.
* Designing a new automation.
* Choosing the correct architectural layer.
* Implementing new functionality.
* Testing.
* Documentation.

This document does not describe any specific automation.

---

# Development Process

Every new automation should follow the same sequence.

```text
Understand
        │
        ▼
Inspect
        │
        ▼
Design
        │
        ▼
Implement
        │
        ▼
Test
        │
        ▼
Document
        │
        ▼
Commit
```

Skipping steps generally results in duplicated code or architectural problems.

---

# Step 1 — Understand the Manual Process

Before writing code, perform the complete process manually.

The objective is to understand:

* every screen involved;
* every user interaction;
* required inputs;
* generated outputs;
* possible failures;
* optional branches.

Do not begin implementation until the complete workflow is understood.

---

# Step 2 — Inspect the Application

Use browser developer tools and Playwright inspection tools to identify:

* stable selectors;
* network requests;
* page transitions;
* downloads;
* modal dialogs;
* asynchronous operations.

Whenever possible, prefer stable semantic selectors over generated identifiers.

Examples include:

* accessible roles;
* labels;
* placeholder text;
* visible text.

Avoid selectors based on dynamic identifiers whenever possible.

---

# Step 3 — Identify the Layers

Determine where each responsibility belongs.

## Core

Choose Core when the functionality is reusable by multiple portals.

Examples:

* download handling;
* browser lifecycle;
* logging;
* common utilities.

---

## Models

Create or extend a model when the business operation requires structured input.

Example:

```python
TrackingFilters(
    school_year="2025-26",
)
```

Avoid long parameter lists.

---

## Page Objects

A Page Object represents a single application screen.

Typical responsibilities:

* click buttons;
* fill forms;
* select values;
* read information.

A Page Object should never coordinate multiple screens.

---

## Workflows

Create a Workflow when the automation spans multiple pages.

Examples:

* authentication;
* report generation;
* export processes.

Workflows coordinate Page Objects.

---

## Portals

Expose only business operations.

Example:

```python
portal.export_tracking_report(filters)
```

The public API should never expose browser interactions.

---

# Step 4 — Implement Incrementally

Avoid implementing an entire automation at once.

Instead, divide the work into small milestones.

Example:

1. Open the page.
2. Navigate to the section.
3. Select filters.
4. Validate results.
5. Export data.
6. Handle failures.

Each milestone should remain executable.

---

# Step 5 — Prefer Reusable Infrastructure

Before adding new code, ask:

> Could this be useful for another automation?

If the answer is yes, it probably belongs in Core.

Examples:

* retries;
* downloads;
* browser utilities;
* common Playwright helpers.

---

# Step 6 — Handle Failures Explicitly

Browser automations should expect failures.

Examples include:

* timeouts;
* expired sessions;
* network delays;
* temporary server errors;
* unexpected dialogs.

Whenever possible:

* retry predictable failures;
* raise meaningful exceptions;
* log useful diagnostic information.

---

# Step 7 — Validate the Result

Execute the complete quality pipeline.

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
uv run mypy automation examples
uv run pytest
```

Then execute the relevant example manually.

Both automated and manual validation are required.

---

# Step 8 — Update Documentation

Every automation should be documented.

At minimum:

* update the README if public capabilities changed;
* update architecture if responsibilities changed;
* create or update automation-specific documentation when appropriate.

Documentation is part of the implementation.

---

# Step 9 — Commit

Commits should represent a single logical change.

Prefer several focused commits over a single large commit.

Examples:

```text
feat(dinantia): navigate to tracking

feat(dinantia): export tracking report

refactor(core): extract download manager

docs: document tracking workflow
```

---

# Choosing the Correct Layer

The following questions help determine where new code belongs.

| Question                             | Layer       |
| ------------------------------------ | ----------- |
| Is it reusable by multiple portals?  | Core        |
| Is it structured business data?      | Models      |
| Does it interact with one screen?    | Page Object |
| Does it coordinate multiple screens? | Workflow    |
| Is it part of the public API?        | Portal      |

If a responsibility seems to belong to multiple layers, reconsider the design.

---

# Common Mistakes

Avoid the following patterns.

## Mixing browser logic with business logic

Incorrect:

```python
page.click(...)
page.wait_for(...)
page.fill(...)
```

inside application code.

---

## Large Page Objects

Page Objects should remain focused on a single screen.

Do not accumulate complete workflows inside them.

---

## Duplicated Infrastructure

If the same browser logic appears in multiple places, extract it into Core.

---

## Long Parameter Lists

Prefer:

```python
TrackingFilters(...)
```

instead of:

```python
export(
    school_year,
    teacher,
    course,
    start_date,
    end_date,
)
```

---

## Skipping Documentation

Documentation is part of the feature.

A feature is not considered complete until its documentation has been updated.

---

# Checklist

Before merging a new automation:

* Manual workflow understood.
* Stable selectors identified.
* Responsibilities assigned to the correct layer.
* Models created where appropriate.
* Workflow implemented.
* Public API updated.
* Quality pipeline passes.
* Manual execution verified.
* Documentation updated.
* Commit created.

---

# Related Documents

* README.md
* architecture.md
* development-guide.md
* testing-and-debugging.md
* documentation-style-guide.md
