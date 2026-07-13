FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install a pinned uv version for reproducible builds
COPY --from=ghcr.io/astral-sh/uv:0.11.28 /uv /usr/local/bin/uv

# Copy dependency metadata first to maximize Docker layer caching
COPY pyproject.toml uv.lock ./

# Install locked production dependencies without installing the project yet
RUN uv sync --frozen --no-dev --no-install-project

# Install Chromium and its required system dependencies
RUN uv run --no-sync playwright install --with-deps chromium

# Copy the application source
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

# Run the application as a non-root user
RUN useradd --create-home automation \
    && chown -R automation:automation /app

USER automation

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "automation.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]