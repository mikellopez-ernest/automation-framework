# Authentication and Sessions

> **Audience:** Developers
>
> **Status:** Stable
>
> **Last Updated:** 2026-07-11
>
> **Applies To:** Browser Authentication

---

# Purpose

This document describes how browser authentication is implemented within the Automation Framework.

It explains the session persistence strategy, the authentication workflow and the rationale behind the architectural decisions adopted by the project.

---

# Scope

This document covers:

* Browser authentication.
* Session persistence.
* Session validation.
* Login fallback.
* Session lifecycle.
* Security considerations.

This document does not describe browser navigation or portal-specific workflows.

---

# Authentication Philosophy

The framework is designed to minimize the number of authentication requests sent to the target application.

Instead of performing a complete login during every execution, browser sessions are persisted and reused whenever possible.

This approach provides three important advantages:

* Faster execution.
* Reduced authentication traffic.
* Lower probability of triggering anti-automation mechanisms.

Authentication should therefore be considered an exceptional operation rather than the default execution path.

---

# Session Lifecycle

The authentication process follows a simple decision flow.

```text
Start
   │
   ▼
Load storage state
   │
   ▼
Session available?
   │
 ┌─┴──────────────┐
 │                │
 ▼                ▼
Yes              No
 │                │
 ▼                ▼
Validate       Perform login
 │                │
 ├─────Valid──────┤
 │                │
 ▼                ▼
Continue      Save new session
                 │
                 ▼
             Continue
```

The framework always attempts to reuse an existing authenticated session before considering a new login.

---

# Storage State

Authenticated browser sessions are persisted using Playwright's **storage state** feature.

The storage state contains:

* authentication cookies;
* local storage;
* session storage (when supported).

This information is sufficient to restore an authenticated browser context without interacting with the login page.

---

# Storage Location

The default session file is stored under:

```text
.playwright/auth/dinantia.json
```

The location is configurable through project settings.

The session file should be considered sensitive information.

---

# Session Validation

Loading a storage state does not guarantee that the session is still valid.

After restoring the browser context, the framework performs an explicit validation step.

The validation process verifies that the authenticated interface is accessible.

If validation succeeds, execution continues normally.

If validation fails, the framework automatically falls back to a complete login.

---

# Login Fallback

Whenever the stored session is missing, invalid or expired, the framework performs a normal browser authentication.

The authentication workflow:

1. Opens the public portal.
2. Navigates to the login page.
3. Completes the login form.
4. Waits for successful authentication.
5. Saves the new storage state.
6. Continues using the newly authenticated session.

The rest of the application remains unaware of this process.

---

# Session Refresh

Sessions are refreshed automatically.

Whenever a login is successfully completed, the existing storage state is replaced with the new authenticated session.

No manual maintenance is required under normal circumstances.

---

# Security Considerations

The storage state should be treated as a credential.

For this reason:

* never commit it to Git;
* never publish it;
* never share it;
* never expose it through logs;
* never include it in documentation examples.

The `.playwright/` directory is excluded from version control.

---

# Configuration

Authentication credentials are stored in the environment configuration.

Typical values include:

* username;
* password;
* storage state path.

Credentials should never appear inside the source code.

---

# Browser Context

Every browser context is created using the stored authentication state whenever available.

This guarantees that all pages opened inside the same context share the authenticated session.

The framework never authenticates individual pages.

Authentication belongs to the browser context.

---

# Failure Scenarios

Typical authentication failures include:

* expired session;
* revoked credentials;
* changed login page;
* unavailable authentication service;
* network failures.

The framework attempts automatic recovery whenever possible.

If recovery is not possible, a business-level exception is raised.

---

# Architectural Decisions

The project intentionally separates authentication from business workflows.

Business operations should never contain login logic.

Instead, authentication is handled before the requested operation begins.

This separation simplifies every workflow and centralizes authentication management.

---

# Future Evolution

Future improvements may include:

* encrypted storage state;
* multiple user profiles;
* automatic session expiration detection;
* support for additional authentication providers;
* optional MFA support where technically feasible.

These improvements should not require changes to business workflows.

---

# Related Documents

* README.md
* architecture.md
* development-guide.md
* dinantia-tracking.md
* ADR-0002 (Persistent Browser Sessions)
