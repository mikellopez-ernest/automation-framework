FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

# Install a pinned uv version for reproducible builds
COPY --from=ghcr.io/astral-sh/uv:0.11.28 /uv /usr/local/bin/uv

# Copy dependency metadata first to maximize Docker layer caching
COPY pyproject.toml uv.lock ./

# Install locked production dependencies without installing the project yet
RUN uv sync --frozen --no-dev --no-install-project

# Install Firefox and its required system dependencies
RUN uv run --no-sync playwright install --with-deps firefox

# Copy the application source
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

RUN useradd --create-home automation \
    && mkdir -p /app/.playwright/auth \
    && chown -R automation:automation /app \
    && chown -R automation:automation /ms-playwright

USER automation

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "automation.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]