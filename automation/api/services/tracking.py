from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from automation.config import Settings
from automation.core import BrowserManager
from automation.models import TrackingFilters
from automation.portals.dinantia import DinantiaPortal

TEMPORARY_DOWNLOAD_PREFIX = "automation-tracking-"


class TrackingService:
    """Application service for Dinantia tracking operations."""

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        self._settings = settings

    def export_report(
        self,
        school_year: str,
    ) -> Path:
        """Export a Dinantia tracking report to a temporary directory."""
        filters = TrackingFilters(
            school_year=school_year,
        )

        download_dir = Path(
            tempfile.mkdtemp(
                prefix=TEMPORARY_DOWNLOAD_PREFIX,
            )
        )

        request_settings = self._settings.model_copy(
            update={
                "download_dir": download_dir,
            }
        )

        try:
            with BrowserManager(
                request_settings.browser,
                request_settings.download_dir,
                storage_state_path=(request_settings.dinantia_storage_state_path),
            ) as browser:
                portal = DinantiaPortal(
                    browser,
                    request_settings,
                )

                report_path = portal.export_tracking_report(
                    filters,
                )

            if not report_path.is_file():
                raise FileNotFoundError(
                    f"Generated report does not exist: {report_path}"
                )

            return report_path

        except Exception:
            shutil.rmtree(
                download_dir,
                ignore_errors=True,
            )
            raise
