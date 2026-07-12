from __future__ import annotations

from pathlib import Path
from typing import cast

from fastapi.testclient import TestClient

from automation.api.app import app
from automation.api.dependencies import (
    get_app_settings,
    get_tracking_service,
)
from automation.api.services import TrackingService
from automation.config import Settings

API_TOKEN = "test-api-token"


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


def override_settings() -> Settings:
    """Return test settings with a configured API token."""
    return Settings(
        _env_file=None,  # type: ignore[call-arg]
        api_token=API_TOKEN,
    )


def authenticated_headers(
    token: str = API_TOKEN,
) -> dict[str, str]:
    """Return API authentication headers."""
    return {
        "Authorization": f"Bearer {token}",
    }


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
        return cast(
            TrackingService,
            fake_service,
        )

    app.dependency_overrides[get_app_settings] = override_settings
    app.dependency_overrides[get_tracking_service] = override_tracking_service

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/dinantia/tracking/export",
            headers=authenticated_headers(),
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


def test_export_tracking_report_rejects_missing_token() -> None:
    app.dependency_overrides[get_app_settings] = override_settings

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/dinantia/tracking/export",
            json={
                "school_year": "2025-26",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {
        "detail": {
            "error": {
                "code": "unauthorized",
                "message": "Invalid or missing API token.",
            }
        }
    }


def test_export_tracking_report_rejects_invalid_token() -> None:
    app.dependency_overrides[get_app_settings] = override_settings

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/dinantia/tracking/export",
            headers=authenticated_headers("invalid-token"),
            json={
                "school_year": "2025-26",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_export_tracking_report_rejects_unconfigured_token() -> None:
    def override_unconfigured_settings() -> Settings:
        return Settings(
            _env_file=None,  # type: ignore[call-arg]
            api_token=None,
        )

    app.dependency_overrides[get_app_settings] = override_unconfigured_settings

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/dinantia/tracking/export",
            headers=authenticated_headers(),
            json={
                "school_year": "2025-26",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "error": {
                "code": "api_token_not_configured",
                "message": "The API token is not configured.",
            }
        }
    }


def test_export_tracking_report_rejects_empty_school_year() -> None:
    app.dependency_overrides[get_app_settings] = override_settings

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/dinantia/tracking/export",
            headers=authenticated_headers(),
            json={
                "school_year": "   ",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_export_tracking_report_removes_temporary_directory(
    tmp_path: Path,
) -> None:
    report_directory = tmp_path / "temporary-report"
    report_directory.mkdir()

    report_path = report_directory / "tracking-report.xlsx"
    report_path.write_bytes(b"test-excel-content")

    fake_service = FakeTrackingService(
        report_path,
    )

    def override_tracking_service() -> TrackingService:
        return cast(
            TrackingService,
            fake_service,
        )

    app.dependency_overrides[get_app_settings] = override_settings
    app.dependency_overrides[get_tracking_service] = override_tracking_service

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/dinantia/tracking/export",
            headers=authenticated_headers(),
            json={
                "school_year": "2025-26",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.content == b"test-excel-content"
    assert not report_directory.exists()
