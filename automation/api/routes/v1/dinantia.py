from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import FileResponse

from automation.api.dependencies import TrackingServiceDependency
from automation.api.schemas import ExportTrackingRequest

router = APIRouter(
    prefix="/dinantia",
    tags=["Dinantia"],
)

EXCEL_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@router.post(
    "/tracking/export",
    response_class=FileResponse,
    summary="Export Dinantia tracking report",
    description=(
        "Generate and download the detailed Dinantia tracking report "
        "for the requested school year."
    ),
    responses={
        200: {
            "description": "Tracking report generated successfully.",
            "content": {
                EXCEL_MEDIA_TYPE: {},
            },
        },
        422: {
            "description": "Invalid request body.",
        },
    },
)
def export_tracking_report(
    request: ExportTrackingRequest,
    service: TrackingServiceDependency,
) -> FileResponse:
    """Generate and return a Dinantia tracking report."""
    report_path = service.export_report(
        request.school_year,
    )

    return FileResponse(
        path=report_path,
        media_type=EXCEL_MEDIA_TYPE,
        filename=report_path.name,
    )
