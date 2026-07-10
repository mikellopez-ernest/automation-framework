# Automation Framework

Reusable browser automation framework built with Python, Playwright and `uv`.

The first supported portal will be Dinantia, but the core package is intentionally portal-agnostic so it can later support Moodle, Clickedu, Google Workspace or other web applications.

## Current milestone

The project currently provides:

- project management with `uv`;
- settings loaded from `.env` using Pydantic Settings;
- centralized logging with Rich;
- a reusable Playwright browser manager;
- Firefox, Chromium and WebKit support;
- a minimal Dinantia example that opens the public home page;
- Ruff, mypy and pytest configuration.

It does not yet perform login or any Dinantia-specific workflow.

## Requirements

- Python 3.11 or newer;
- `uv`;
- macOS or Linux.

## Installation

```bash
unzip automation_framework.zip
cd automation_framework
uv sync --dev
uv run playwright install firefox chromium
```

For Ubuntu Server, install the browser and its operating-system dependencies with:

```bash
uv run playwright install --with-deps firefox chromium
```

## Configuration

Create the local `.env` file:

```bash
cp .env.example .env
```

Default development configuration:

```dotenv
AUTOMATION_BROWSER_ENGINE=firefox
AUTOMATION_BROWSER_HEADLESS=false
AUTOMATION_BROWSER_TIMEOUT_MS=30000
AUTOMATION_BROWSER_SLOW_MO_MS=0
AUTOMATION_LOG_LEVEL=INFO
AUTOMATION_DOWNLOAD_DIR=downloads
```

For Ubuntu Server:

```dotenv
AUTOMATION_BROWSER_HEADLESS=true
```

The `.env` file is ignored by Git.

## Run the first example

```bash
uv run python examples/dinantia_open_home.py
```

The command should open Firefox, load Dinantia and print the page title.

## Quality checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy automation examples
uv run pytest
```

To automatically format the code:

```bash
uv run ruff format .
```

## Project structure

```text
automation_framework/
├── automation/
│   ├── config/
│   │   ├── loader.py
│   │   └── settings.py
│   ├── core/
│   │   ├── browser.py
│   │   ├── exceptions.py
│   │   └── logger.py
│   └── portals/
│       └── dinantia/
│           └── constants.py
├── examples/
│   └── dinantia_open_home.py
├── tests/
│   └── test_settings.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## First Git commit

After verifying that the example works:

```bash
git init
git add .
git commit -m "Create automation framework foundation"
```

## Next milestone

The next commit will add a Dinantia home-page object that:

1. rejects the cookie prompt;
2. clicks the `Sign in` link;
3. verifies that the login page opens in a new browser page.
