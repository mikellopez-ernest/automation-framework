# Roadmap

> Last updated: 2026-07-13

---

# Vision

Automation Framework is intended to become a reusable platform for exposing browser automations through a consistent HTTP API.

The long-term objective is to integrate multiple external platforms while keeping the underlying framework independent from any specific provider.

---

# Guiding Principles

Future development should always preserve the following principles:

- Layered architecture
- Strong typing
- Business-oriented APIs
- Reusable infrastructure
- Comprehensive documentation
- High test coverage
- Minimal coupling between providers

Framework improvements should benefit every automation rather than solving isolated problems.

---

# Phase 1 — Framework

**Status:** ✅ Completed

## Objectives

- Browser abstraction
- Download infrastructure
- Configuration system
- Logging
- Exception hierarchy
- Typed models
- Workflow abstraction
- Portal abstraction

## Result

A reusable browser automation framework independent from any specific portal.

---

# Phase 2 — Dinantia Integration

**Status:** ✅ Completed

## Objectives

- Authentication
- Persistent sessions
- Tracking navigation
- School year selection
- Detailed tracking
- Excel export
- Automatic retry strategy

## Result

Production-ready Dinantia tracking automation.

---

# Phase 3 — HTTP API

**Status:** ✅ Completed

## Objectives

- FastAPI application
- Versioned API
- OpenAPI
- Swagger UI
- Dependency injection
- Service layer
- Bearer authentication
- Exception handlers
- Serialized execution
- Temporary downloads
- End-to-end validation

## Result

A production-ready HTTP API exposing browser automations.

---

# Phase 4 — Deployment

**Status:** 🟡 In Progress

## Objectives

- Docker image
- Docker Compose
- Reverse proxy
- HTTPS
- Production configuration
- Deployment guide
- Backup strategy
- Health monitoring

## Expected Result

Self-contained deployment suitable for production environments.

---

# Phase 5 — Google Apps Script

**Status:** ⏳ Planned

## Objectives

- GAS client library
- Authentication wrapper
- File download helper
- Error handling
- Documentation
- Usage examples

## Expected Result

Browser automations consumable directly from Google Apps Script.

---

# Phase 6 — New Automations

**Status:** ⏳ Planned

Future Dinantia automations may include:

- Incidents
- Messages
- Student information
- Family communications
- Attendance
- Administrative reports

Every new automation must reuse the existing framework.

---

# Phase 7 — Additional Providers

**Status:** ⏳ Planned

Potential future integrations:

- Untis
- Moodle
- Microsoft 365
- Google Workspace
- Other educational platforms

Each provider should implement only:

- Page Objects
- Workflows
- Portal

No framework changes should be required.

---

# Phase 8 — Production Features

**Status:** ⏳ Planned

Possible future improvements:

- Request queue
- Background jobs
- Metrics
- Monitoring
- Structured logging
- API rate limiting
- Multi-user authentication
- Audit logging

These features should only be implemented when justified by operational needs.

---

# Long-Term Goals

The framework should eventually provide:

- Multiple automation providers
- Stable HTTP API
- Well-defined domain models
- Reusable client libraries
- Production-grade deployment
- Comprehensive documentation

The browser automation engine should remain an implementation detail hidden behind the API.

---

# Out of Scope

The following are intentionally outside the scope of the framework:

- Web scraping unrelated to business workflows
- GUI desktop applications
- Generic RPA tooling
- Browser automation scripting
- Low-level Playwright wrappers

The project focuses on exposing business operations, not browser interactions.

---

# Success Criteria

The project can be considered mature when:

- New providers can be added without modifying the framework.
- Browser automation remains completely hidden behind public APIs.
- Every public operation is documented and tested.
- Production deployment requires minimal configuration.
- External systems interact exclusively through HTTP APIs.

---

# Current Priority

Current development is focused on deployment.

Next milestone:

```
Docker
        ↓
Docker Compose
        ↓
HTTPS
        ↓
Google Apps Script client
```