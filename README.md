# Automation Framework

**Status:** Active Development

**Language:** Python 3.11+

**Automation Engine:** Playwright

**Package Manager:** uv

**Code Quality:** Ruff · MyPy · Pytest

**Primary Target:** Dinantia Student Tracking

**API Layer:** FastAPI (planned)

---

## Overview

Automation Framework is a Python framework for building reliable browser automations on top of Playwright.

The project was originally created to automate functionality that is not exposed through public APIs while maintaining a clean, reusable architecture. Although the first supported portal is **Dinantia**, the framework is designed to keep reusable infrastructure independent from portal-specific implementations.

Its primary goal is to expose high-level business operations instead of browser interactions, allowing external systems such as Google Apps Script to consume browser automations through a simple API.

---

## Project Goals

The framework has been designed around a small set of principles:

* Build reliable browser automations using Playwright.
* Isolate reusable infrastructure from portal-specific implementations.
* Expose business-oriented APIs instead of browser operations.
* Minimize maintenance when target applications change.
* Support integration with external services through HTTP APIs.
* Maintain production-quality code, tests and documentation.

---

## Current Status

| Portal   | Feature                                |   Status   |
| -------- | -------------------------------------- | :--------: |
| Dinantia | Authentication with persistent session |      ✅     |
| Dinantia | Student tracking navigation            |      ✅     |
| Dinantia | School year selection                  |      ✅     |
| Dinantia | Detailed tracking view                 |      ✅     |
| Dinantia | Report export with automatic retry     |      ✅     |
| FastAPI  | HTTP API                               | 🚧 Planned |

---

## Architecture Overview

The project follows a layered architecture where every layer has a single responsibility.

```text
Applications
        │
        ▼
DinantiaPortal
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
```

Responsibilities are distributed as follows:

* **Core** contains reusable infrastructure such as browser management, downloads, logging and configuration.
* **Page Objects** encapsulate the behaviour of individual application screens.
* **Workflows** coordinate multiple page objects to perform complete business operations.
* **Portals** expose a simple public API while hiding implementation details.

For a detailed explanation of the architecture, see **docs/architecture.md**.

---

## Project Structure

```text
automation/
├── config/
├── core/
├── models/
├── portals/
├── workflows/
├── examples/
├── tests/
└── docs/
```

| Directory     | Purpose                                               |
| ------------- | ----------------------------------------------------- |
| **config**    | Application configuration and environment settings    |
| **core**      | Reusable infrastructure shared by every automation    |
| **models**    | Typed domain models used by workflows and public APIs |
| **portals**   | Portal-specific implementations                       |
| **workflows** | Business workflows composed of multiple page objects  |
| **examples**  | Minimal executable examples                           |
| **tests**     | Automated test suite                                  |
| **docs**      | Project documentation                                 |

---

## Quick Start

### Clone the repository

```bash
git clone <repository-url>
cd automation
```

### Install dependencies

```bash
uv sync --dev
```

### Install Playwright browsers

```bash
uv run playwright install
```

### Configure the environment

```bash
cp .env.example .env
```

Edit the `.env` file with the appropriate credentials and configuration values.

### Run the example

```bash
uv run python examples/dinantia_login.py
```

---

## Example

The public API intentionally remains small and business-oriented.

```python
from automation.config.loader import get_settings
from automation.core.browser import BrowserManager
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

The example contains no Playwright selectors, browser waits or navigation logic. Those responsibilities remain entirely inside the framework.

---

## Development

Before committing changes, run the complete quality pipeline:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
uv run mypy automation examples
uv run pytest
```

---

## Documentation

Project documentation is located in the **docs/** directory.

| Document                         | Description                                     |
| -------------------------------- | ----------------------------------------------- |
| `documentation-style-guide.md`   | Documentation conventions and writing standards |
| `architecture.md`                | Project architecture                            |
| `development-guide.md`           | Development workflow                            |
| `dinantia-tracking.md`           | Tracking automation design                      |
| `authentication-and-sessions.md` | Session persistence                             |
| `adding-a-new-automation.md`     | Extending the framework                         |
| `testing-and-debugging.md`       | Debugging and troubleshooting                   |

---

## Roadmap

Planned improvements include:

* FastAPI service layer
* Google Apps Script integration
* Docker deployment
* Additional Dinantia tracking automations
* Richer domain models
* Expanded automated test suite

---

## License

Private project.
