# ADR-0004 — Reusable Download Infrastructure

> **Status:** Accepted
>
> **Date:** 2026-07-11

---

# Context

Downloading files is a common operation in browser automations.

Different portals may expose downloads through different user interfaces, but the underlying concerns remain the same:

* waiting for downloads;
* preserving filenames;
* avoiding overwriting files;
* retrying temporary failures;
* handling browser behaviour consistently.

Duplicating this logic across automations would increase maintenance costs.

---

# Decision

Download management is implemented as reusable Core infrastructure.

Portal implementations are responsible only for initiating the download.

All download lifecycle management remains centralized within reusable components.

---

# Consequences

Positive:

* Consistent download behaviour.
* Reduced code duplication.
* Easier future extensions.
* Simpler portal implementations.

Negative:

* Slight increase in abstraction.
* Core infrastructure grows over time.

---

# Related Documents

* architecture.md
* development-guide.md
* dinantia-tracking.md
