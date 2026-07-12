from __future__ import annotations

from fastapi import APIRouter

from automation.api.schemas import RootResponse

router = APIRouter()


@router.get(
    "/",
    response_model=RootResponse,
    summary="API information",
    description="Return basic information about the Automation Framework API.",
)
def root() -> RootResponse:
    """Return API metadata."""
    return RootResponse(
        service="Automation Framework",
        version="0.1.0",
        status="running",
    )
