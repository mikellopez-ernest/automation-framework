from __future__ import annotations

from fastapi import APIRouter

from automation.api.schemas import HealthResponse

router = APIRouter(
    tags=["Health"],
)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check service health",
    description=(
        "Verify that the HTTP service is running. "
        "This endpoint does not launch a browser or connect to Dinantia."
    ),
)
def health_check() -> HealthResponse:
    """Return the current service health."""
    return HealthResponse(
        status="ok",
    )
