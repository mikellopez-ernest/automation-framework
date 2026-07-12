from __future__ import annotations

from fastapi import FastAPI

from .routes import (
    health_router,
    root_router,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title="Automation Framework",
        description="Reusable browser automation API.",
        version="0.1.0",
    )

    app.include_router(
        root_router,
    )

    app.include_router(
        health_router,
    )

    return app
