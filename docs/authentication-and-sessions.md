# Authentication and Sessions

> Status: Stable
>
> Last updated: 2026-07-13

---

# Overview

Automation Framework uses two completely independent authentication mechanisms.

They serve different purposes and should never be confused.

```
HTTP Client

↓

Bearer Authentication

↓

Automation Framework

↓

Playwright

↓

Dinantia Authentication
```

External clients authenticate against the API.

The browser authenticates independently against Dinantia.

---

# Authentication Layers

## API Authentication

The HTTP API is protected using a static Bearer token.

Clients must send:

```
Authorization: Bearer <API_TOKEN>
```

The expected token is configured through:

```
AUTOMATION_API_TOKEN
```

This authentication occurs before:

- request validation
- browser startup
- dependency execution
- Playwright initialization

Invalid requests never start a browser.

---

## Dinantia Authentication

Dinantia authentication is completely independent from the HTTP API.

The framework authenticates using:

```
Username

↓

Password

↓

Persistent Browser Session
```

Configuration:

```
AUTOMATION_DINANTIA_USERNAME

AUTOMATION_DINANTIA_PASSWORD
```

These credentials are never exposed to API clients.

---

# Session Persistence

Successful authentication generates a persistent Playwright storage state.

Default location:

```
.playwright/auth/dinantia.json
```

The storage state contains:

- cookies
- local storage
- session storage

Passwords are never stored.

---

# Browser Startup

Every automation request follows this sequence.

```
Receive HTTP request

↓

Validate Bearer token

↓

Acquire automation lock

↓

Start BrowserManager

↓

Load storage state

↓

Reuse existing session

↓

Execute automation
```

Whenever possible, the login page is skipped.

---

# Automatic Login

If the stored browser session is invalid:

```
Load storage state

↓

Session expired

↓

Open login page

↓

Authenticate

↓

Save new storage state

↓

Continue automation
```

The process is completely transparent to the API client.

---

# Storage State Lifecycle

```
First login

↓

Save storage state

↓

Subsequent requests

↓

Reuse session

↓

Session expires

↓

Authenticate again

↓

Replace storage state
```

Only one storage state is maintained for the current Dinantia account.

---

# Browser Lifetime

Browser instances are intentionally short-lived.

Each HTTP request:

- creates a browser
- executes the automation
- closes the browser

Only the authentication state is persistent.

This approach minimizes:

- memory usage
- browser instability
- stale browser contexts

---

# Security Considerations

## API Token

The Bearer token should:

- be randomly generated
- never be committed to Git
- never appear in logs
- only be stored in environment variables

Example:

```bash
openssl rand -hex 32
```

---

## Dinantia Credentials

Dinantia credentials should only exist in:

```
.env
```

They should never be:

- hardcoded
- logged
- returned through the API

---

## Storage State

The browser session should be considered sensitive.

Recommended:

- exclude from Git
- backup securely if needed
- protect filesystem permissions

Anyone with access to the storage state may be able to reuse the authenticated session.

---

# Error Scenarios

## Missing API Token

Result:

```
401 Unauthorized
```

Browser is never started.

---

## Invalid API Token

Result:

```
401 Unauthorized
```

Browser is never started.

---

## API Token Not Configured

Result:

```
503 Service Unavailable
```

The framework refuses to serve requests.

---

## Invalid Dinantia Credentials

Result:

```
502 Bad Gateway
```

The browser attempted to authenticate but the external platform rejected the credentials.

---

## Expired Session

The framework automatically attempts a fresh login.

If authentication succeeds:

- storage state is replaced
- automation continues normally

No manual intervention is normally required.

---

# Authentication Flow

```
HTTP Request

↓

Bearer Authentication

↓

Automation Lock

↓

Browser Startup

↓

Load Storage State

↓

Session Valid?

├── Yes
│
│   Continue
│
└── No
    │
    ▼
Authenticate

↓

Save Storage State

↓

Continue Automation
```

---

# Configuration

Required variables:

```
AUTOMATION_API_TOKEN

AUTOMATION_DINANTIA_USERNAME

AUTOMATION_DINANTIA_PASSWORD
```

Optional:

```
AUTOMATION_DINANTIA_STORAGE_STATE_PATH
```

The default storage location is suitable for most deployments.

---

# Best Practices

- Generate a strong API token.
- Protect the storage state file.
- Never expose credentials through logs.
- Keep browser sessions persistent.
- Keep browser instances ephemeral.
- Separate API authentication from Dinantia authentication.

---

# Related Documentation

- architecture.md
- api-design.md
- development-guide.md