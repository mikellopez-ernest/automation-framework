from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from automation.api.locks import AutomationBusyError
from automation.core.exceptions import (
    AuthenticationError,
    AutomationError,
    BrowserError,
    DinantiaExportError,
    DinantiaTrackingError,
    DownloadError,
    ValidationError,
)

logger = logging.getLogger(__name__)

ExceptionHandler = Callable[
    [Request, Exception],
    Awaitable[JSONResponse],
]


def register_exception_handlers(app: FastAPI) -> None:
    """Register framework exception handlers in the FastAPI application."""
    app.add_exception_handler(
        ValidationError,
        _create_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="validation_error",
            public_message="The supplied data is invalid.",
        ),
    )

    app.add_exception_handler(
        AuthenticationError,
        _create_handler(
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="dinantia_authentication_failed",
            public_message="Dinantia authentication failed.",
        ),
    )

    app.add_exception_handler(
        DinantiaExportError,
        _create_handler(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="dinantia_export_failed",
            public_message="Dinantia could not generate the tracking report.",
        ),
    )

    app.add_exception_handler(
        DinantiaTrackingError,
        _create_handler(
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="dinantia_tracking_failed",
            public_message="The Dinantia tracking operation failed.",
        ),
    )

    app.add_exception_handler(
        DownloadError,
        _create_handler(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="download_failed",
            public_message="The generated file could not be downloaded.",
        ),
    )

    app.add_exception_handler(
        BrowserError,
        _create_handler(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="browser_unavailable",
            public_message="The browser automation service is unavailable.",
        ),
    )

    app.add_exception_handler(
        AutomationBusyError,
        _create_handler(
            status_code=status.HTTP_409_CONFLICT,
            error_code="automation_busy",
            public_message="Another automation is currently running.",
        ),
    )

    app.add_exception_handler(
        AutomationError,
        _create_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="automation_error",
            public_message="The automation operation failed.",
        ),
    )

    app.add_exception_handler(
        Exception,
        _unexpected_exception_handler,
    )


def _create_handler(
    *,
    status_code: int,
    error_code: str,
    public_message: str,
) -> ExceptionHandler:
    """Create an HTTP handler for a framework exception."""

    async def handler(
        request: Request,
        exception: Exception,
    ) -> JSONResponse:
        logger.error(
            "API request failed: method=%s path=%s error_type=%s error=%s",
            request.method,
            request.url.path,
            type(exception).__name__,
            exception,
            exc_info=exception,
        )

        return _error_response(
            status_code=status_code,
            error_code=error_code,
            message=public_message,
        )

    return handler


async def _unexpected_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    """Handle unexpected exceptions without exposing internal details."""
    logger.exception(
        "Unexpected API error: method=%s path=%s",
        request.method,
        request.url.path,
        exc_info=exception,
    )

    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="internal_server_error",
        message="An unexpected internal error occurred.",
    )


def _error_response(
    *,
    status_code: int,
    error_code: str,
    message: str,
) -> JSONResponse:
    """Build the standard API error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": message,
            }
        },
    )
