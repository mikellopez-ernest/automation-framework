# Automation Framework

**Status:** Production Ready

**Language:** Python 3.11+

**Automation Engine:** Playwright

**HTTP API:** FastAPI

**Package Manager:** uv

**Code Quality:** Ruff · MyPy · Pytest

**Primary Integration:** Dinantia

---

# Overview

Automation Framework is a reusable Python framework for building reliable browser automations and exposing them through a clean HTTP API.

The framework is designed around business operations rather than browser interactions. Consumers never interact with Playwright directly; instead they use high-level services such as exporting a Dinantia tracking report.

Although the first supported platform is **Dinantia**, the architecture is intentionally provider-agnostic. Additional portals can be incorporated without changing the overall framework or API architecture.

Typical consumers include:

- Google Apps Script
- Internal web applications
- Scheduled automation services
- Other Python applications

---

# Project Goals

The project is built around a small set of engineering principles.

- Build reliable browser automations using Playwright.
- Expose business-oriented APIs instead of browser operations.
- Isolate reusable infrastructure from portal-specific implementations.
- Keep every architectural layer focused on a single responsibility.
- Maintain production-quality documentation, testing and static analysis.
- Make new automations inexpensive to develop.

---

# Current Status

## Framework

| Feature | Status |
|----------|:------:|
| Browser management | ✅ |
| Download infrastructure | ✅ |
| Configuration | ✅ |
| Exception hierarchy | ✅ |
| Logging | ✅ |
| Typed domain models | ✅ |
| Workflow layer | ✅ |
| Portal layer | ✅ |

## Dinantia

| Feature | Status |
|----------|:------:|
| Authentication | ✅ |
| Persistent sessions | ✅ |
| Tracking navigation | ✅ |
| School year selection | ✅ |
| Detailed tracking view | ✅ |
| Report export | ✅ |
| Automatic download retry | ✅ |

## HTTP API

| Feature | Status |
|----------|:------:|
| FastAPI application | ✅ |
| OpenAPI | ✅ |
| Swagger UI | ✅ |
| API versioning | ✅ |
| Response schemas | ✅ |
| Service layer | ✅ |
| Tracking export endpoint | ✅ |
| Bearer authentication | ✅ |
| Exception handlers | ✅ |
| Concurrency lock | ✅ |

---

# Architecture

The project follows a layered architecture.

Each layer has a single responsibility.

```text
Applications

        │
        ▼

HTTP API

        │
        ▼

Routers

        │
        ▼

Services

        │
        ▼

Portals

        │
        ▼

Workflows

        │
        ▼

Page Objects

        │
        ▼

Core Infrastructure

        │
        ▼

Playwright

        │
        ▼

External Platform
```

Responsibilities are intentionally isolated.

| Layer | Responsibility |
|--------|----------------|
| **API** | HTTP transport |
| **Routers** | Request parsing and response generation |
| **Services** | Application orchestration |
| **Portals** | Public business API |
| **Workflows** | Multi-page business operations |
| **Page Objects** | Individual screens |
| **Core** | Shared infrastructure |

No Playwright code should exist above the Page Object layer.

For additional details see:

- `docs/architecture.md`

---

# Project Structure

```text
```text
.
├── automation/
├── docs/
├── infrastructure/
│   └── caddy/
├── tests/
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

| Directory          | Purpose                          |
| ------------------ | -------------------------------- |
| **automation**     | Framework source code            |
| **docs**           | Project documentation            |
| **infrastructure** | Shared deployment infrastructure |
| **tests**          | Test suite                       |


---

# Quick Start

## Clone

```bash
git clone <repository-url>
cd automation
```

---

## Install dependencies

```bash
uv sync --dev
```

---

## Install Playwright

```bash
uv run playwright install
```

---

## Configure

```bash
cp .env.example .env
```

Edit the configuration values.

---

## Run an example

```bash
uv run python examples/dinantia_login.py
```

---

## Start the HTTP API

```bash
uv run uvicorn automation.api.app:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

OpenAPI:

```
http://127.0.0.1:8000/openapi.json
```

---

# Production Deployment

Production deployments are split into two independent Docker Compose stacks.

The application stack contains only Automation Framework.

Shared infrastructure components, such as the reverse proxy, are located under:

```text
infrastructure/
```

The current infrastructure includes:

* Caddy reverse proxy
* Automatic HTTPS
* TLS certificate management

Applications communicate through a shared external Docker network named:

```text
proxy
```

See:

* `docs/deployment.md`


The deployment guide includes:

* installation;
* environment configuration;
* HTTPS configuration;
* backups;
* disaster recovery;
* operational procedures;
* security considerations.

# Python Example

```python
from automation.config import get_settings
from automation.core import BrowserManager
from automation.models import TrackingFilters
from automation.portals.dinantia import DinantiaPortal

settings = get_settings()

filters = TrackingFilters(
    school_year="2025-26",
)

with BrowserManager(
    settings.browser,
    settings.download_dir,
    storage_state_path=settings.dinantia_storage_state_path,
) as browser:

    portal = DinantiaPortal(
        browser,
        settings,
    )

    report = portal.export_tracking_report(
        filters,
    )

print(report)
```

Consumers never interact directly with Playwright.

---

# HTTP API

Current endpoints:

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/v1/dinantia/tracking/export` | Export tracking report |

Interactive documentation is automatically generated through FastAPI.

---

# Development

Run the complete quality pipeline before committing.

```bash
uv run ruff check . --fix

uv run ruff format .

uv run ruff check .

uv run mypy

uv run pytest
```

The repository should always remain green.

---

# Documentation

The complete documentation is located under `docs/`.

## Documentation Map

| Area | Main Document |
|------|---------------|
| Architecture | architecture.md |
| Development | development-guide.md |
| Deployment | deployment.md |
| API | api-design.md |
| Testing | testing-and-debugging.md |
| ADRs | decisions/ |

## Getting Started

| Document | Description |
|----------|-------------|
| `project-status.md` | Current development status |
| `roadmap.md` | Project roadmap |
| `architecture.md` | System architecture |
| `development-guide.md` | Development workflow |
| `deployment.md` | Production deployment guide |
| `infrastructure/README.md` | Shared deployment infrastructure |

## Framework

| Document | Description |
|----------|-------------|
| `authentication-and-sessions.md` | Session management |
| `adding-a-new-automation.md` | Creating new automations |
| `dinantia-tracking.md` | Dinantia tracking implementation |
| `testing-and-debugging.md` | Testing and troubleshooting |

## API

| Document | Description |
|----------|-------------|
| `api-design.md` | HTTP API contract |

## Engineering

| Document | Description |
|----------|-------------|
| `documentation-style-guide.md` | Documentation conventions |
| `decisions/` | Architectural Decision Records (ADR) |

---

# Contributing

Development standards are defined in:

```
AGENTS.md
```

Every contributor (human or AI) should read this document before modifying the project.

---

# License

Private project.