from __future__ import annotations

from pathlib import Path

from automation.config.settings import Settings
from automation.core.browser import BrowserManager
from automation.workflows.dinantia.tracking_export import (
    export_tracking_report,
)


class DinantiaPortal:
    """High-level facade for Dinantia automations."""

    def __init__(
        self,
        browser: BrowserManager,
        settings: Settings,
    ) -> None:
        self._browser = browser
        self._settings = settings

    def export_tracking_report(
        self,
        school_year: str,
    ) -> Path:
        """Export the detailed tracking report for a school year."""
        return export_tracking_report(
            self._browser,
            self._settings,
            school_year,
        )
