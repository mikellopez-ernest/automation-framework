from __future__ import annotations

from pathlib import Path

from automation.config import Settings
from automation.core import BrowserManager
from automation.models import TrackingFilters
from automation.portals.dinantia import DinantiaPortal


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
        """Export a Dinantia tracking report."""
        filters = TrackingFilters(
            school_year=school_year,
        )

        with BrowserManager(
            self._settings.browser,
            self._settings.download_dir,
            storage_state_path=self._settings.dinantia_storage_state_path,
        ) as browser:
            portal = DinantiaPortal(
                browser,
                self._settings,
            )

            return portal.export_tracking_report(
                filters,
            )
