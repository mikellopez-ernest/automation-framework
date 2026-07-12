from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from automation.api.app import app
from automation.api.dependencies import get_tracking_service
from automation.api.services import TrackingService


class FakeTrackingService:
    """Test double for tracking exports."""

    def __init__(self, report_path: Path) -> None:
        self._report_path = report_path
        self.received_school_year: str | None = None

    def export_report(
        self,
        school_year: str,
    ) -> Path:
        self.received_school_year = school_year
        return self._report_path


def test_export_tracking_report_returns_file(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "tracking-report.xlsx"
    report_content = b"test-excel-content"
    report_path.write_bytes(report_content)

    fake_service = FakeTrackingService(
        report_path,
    )

    def override_tracking_service() -> TrackingService:
        return fake_service  # type: ignore[return-value]

    app.dependency_overrides[get_tracking_service] = override_tracking_service

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/dinantia/tracking/export",
            json={
                "school_year": " 2025-26 ",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.content == report_content
    assert fake_service.received_school_year == "2025-26"
    assert (
        response.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
    assert "tracking-report.xlsx" in response.headers["content-disposition"]


def test_export_tracking_report_rejects_empty_school_year() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/dinantia/tracking/export",
        json={
            "school_year": "   ",
        },
    )

    assert response.status_code == 422
