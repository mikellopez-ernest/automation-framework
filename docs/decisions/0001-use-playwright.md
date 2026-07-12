# ADR-0001 — Use Playwright

> **Status:** Accepted
>
> **Date:** 2026-07-11

---

# Context

The project requires reliable browser automation for web applications that do not expose all required functionality through public APIs.

The selected automation library must provide:

* modern browser support;
* reliable element interaction;
* automatic waiting mechanisms;
* download handling;
* browser context isolation;
* persistent authenticated sessions;
* long-term maintainability.

Alternative technologies considered included Selenium.

---

# Decision

The project uses **Playwright** as the browser automation engine.

Playwright is treated as an implementation detail.

Only the framework interacts directly with Playwright APIs.

Applications consume high-level business operations exposed by the framework instead of browser interactions.

---

# Consequences

Positive:

* Modern browser automation.
* Reliable synchronization.
* Native download support.
* Storage state persistence.
* Consistent API across browsers.
* Excellent developer tooling.

Negative:

* Additional browser installation required.
* Tighter dependency on Playwright APIs.
* Limited support for very old browsers.

---

# Related Documents

* architecture.md
* development-guide.md
* testing-and-debugging.md
