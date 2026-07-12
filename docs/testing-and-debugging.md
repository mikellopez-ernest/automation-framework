# Testing and Debugging

> **Audience:** Developers
>
> **Status:** Stable
>
> **Last Updated:** 2026-07-11
>
> **Applies To:** Entire project

---

# Purpose

This document describes the testing strategy and debugging techniques used throughout the Automation Framework.

Rather than providing a generic Playwright guide, it documents the real issues encountered during development and the techniques used to diagnose and resolve them.

---

# Scope

This document covers:

* Development validation.
* Browser debugging.
* Playwright troubleshooting.
* Common failure scenarios.
* Diagnostic techniques.

This document does not describe individual business workflows.

---

# Testing Philosophy

Testing is performed at multiple levels.

No single technique is considered sufficient.

Every significant change should be validated through:

* Static analysis.
* Type checking.
* Automated tests.
* Manual execution.

Together these provide confidence that the framework behaves correctly.

---

# Quality Pipeline

Before every commit execute:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
uv run mypy automation examples
uv run pytest
```

Whenever browser behaviour changes, execute the relevant example manually.

---

# Manual Verification

Browser automations interact with external systems.

For this reason, automated tests cannot verify every scenario.

Important workflows should always be executed manually after implementation.

Manual verification confirms:

* navigation;
* browser interaction;
* downloads;
* authentication;
* application behaviour.

---

# Debug Configuration

During development the browser should normally run with:

* headless disabled;
* slow motion disabled unless required;
* detailed logging enabled.

Watching the browser frequently reveals problems that logs alone cannot explain.

---

# Logging

Logs should describe business operations rather than browser operations.

Good examples:

```text
Opening tracking page

Selecting school year

Export attempt 2 of 3

Download completed
```

Avoid logging individual clicks or selectors unless debugging.

Logs should explain what the framework is trying to accomplish.

---

# Common Failure Scenarios

The following issues have been observed during development.

---

## Session Expired

Symptoms:

* Redirect to login.
* Missing authenticated interface.

Resolution:

The framework automatically performs a new login and refreshes the stored session.

---

## Dynamic Identifiers

Observed behaviour:

Many elements receive dynamically generated identifiers.

Example:

```text
uid-9-password
uid-14-password
uid-...
```

Recommendation:

Never use generated identifiers as selectors.

Prefer semantic selectors.

---

## Multiple Matching Elements

Observed behaviour:

Some pages contain multiple elements matching the same placeholder or visible text.

Example:

Two Email fields may exist simultaneously.

Recommendation:

Reduce the search scope before interacting with elements.

---

## AJAX Intermediate Responses

Observed behaviour:

A single user action may trigger multiple requests.

Example:

```text
POST /web/attitude/get_chart_data
```

The first response may contain no records while later responses contain the complete dataset.

Recommendation:

Validate response contents instead of assuming the first response is final.

---

## Export Failure

Observed behaviour:

Export occasionally opens a temporary browser tab displaying an HTTP 500 error.

Recommendation:

Close the temporary page.

Retry the export.

Do not immediately consider this an automation failure.

---

## Browser Timeouts

A timeout does not necessarily indicate a slow application.

Possible causes include:

* incorrect selector;
* hidden element;
* unexpected navigation;
* incorrect frame;
* application state.

Always investigate the real cause before increasing timeout values.

---

# Debugging Strategy

When a new issue appears, investigate in the following order.

## 1. Observe

Watch the browser.

Determine exactly where execution stops.

---

## 2. Inspect

Use browser developer tools.

Verify:

* element existence;
* visibility;
* enabled state;
* page structure.

---

## 3. Verify Selectors

Confirm that selectors still match the application.

Prefer semantic selectors.

Avoid generated identifiers.

---

## 4. Verify Network Activity

Check whether browser requests complete successfully.

Unexpected network behaviour often explains browser failures.

---

## 5. Improve Logging

If the cause remains unclear, improve logging before changing implementation.

Logs should describe application state rather than implementation details.

---

# Playwright Inspector

Whenever necessary, Playwright's inspection tools may be used to:

* inspect selectors;
* experiment with locators;
* validate browser interactions.

Inspection tools should be considered part of the normal development workflow.

---

# Browser Console

When diagnosing unexpected behaviour, inspect:

* JavaScript errors;
* failed network requests;
* browser warnings.

Application-side errors frequently explain automation failures.

---

# Retry Policy

Retries should only be implemented when failures are known to be temporary.

Examples:

* intermittent server errors;
* transient network failures;
* delayed downloads.

Retries should never hide programming errors.

---

# When Not to Retry

Do not retry:

* invalid selectors;
* authentication failures caused by invalid credentials;
* missing application features;
* programming errors.

These require investigation rather than repetition.

---

# Principles

When debugging:

Prefer observation over assumptions.

Prefer application events over fixed delays.

Prefer semantic selectors over fragile selectors.

Prefer improving the implementation over increasing timeouts.

---

# Related Documents

* README.md
* architecture.md
* development-guide.md
* adding-a-new-automation.md
* dinantia-tracking.md
* authentication-and-sessions.md
