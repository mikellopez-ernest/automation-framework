# ADR-0002 — Persist Browser Sessions

> **Status:** Accepted
>
> **Date:** 2026-07-11

---

# Context

Executing a complete login before every automation introduces unnecessary browser interactions, increases execution time and may increase the likelihood of triggering anti-automation protections.

Browser sessions can be persisted using Playwright storage state.

---

# Decision

Authenticated sessions are stored and restored using Playwright storage state.

Every execution follows this strategy:

1. Load stored session.
2. Validate authentication.
3. Continue if valid.
4. Perform a complete login only if necessary.
5. Replace the stored session after successful authentication.

Authentication is therefore considered a recovery mechanism rather than the normal execution path.

---

# Consequences

Positive:

* Faster execution.
* Reduced authentication traffic.
* Lower risk of account restrictions.
* Centralized authentication logic.

Negative:

* Session files must be protected.
* Sessions may expire unexpectedly.
* Session validation becomes mandatory.

---

# Related Documents

* authentication-and-sessions.md
* dinantia-tracking.md
