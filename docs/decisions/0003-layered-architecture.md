# ADR-0003 — Layered Architecture

> **Status:** Accepted
>
> **Date:** 2026-07-11

---

# Context

Browser automations naturally combine browser interactions, business logic and reusable infrastructure.

Without clear architectural boundaries these responsibilities quickly become mixed, making maintenance increasingly difficult.

---

# Decision

The project adopts a layered architecture.

```
Applications
        │
Portals
        │
Workflows
        │
Page Objects
        │
Core
        │
Playwright
```

Each layer owns a single responsibility.

Dependencies are allowed only from higher layers to lower layers.

Circular dependencies are not permitted.

---

# Consequences

Positive:

* Clear separation of concerns.
* Predictable project structure.
* Easier maintenance.
* Better testability.
* Reusable infrastructure.

Negative:

* Slightly more files.
* Additional abstraction for small features.

---

# Related Documents

* architecture.md
* adding-a-new-automation.md
