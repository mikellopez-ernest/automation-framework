from __future__ import annotations

import logging
from pathlib import Path

from automation.config.settings import Settings
from automation.core.browser import BrowserManager
from automation.portals.dinantia.detail import DinantiaDetailPage
from automation.portals.dinantia.tracking import DinantiaTrackingPage

from .authentication import open_authenticated_dinantia_page

logger = logging.getLogger(__name__)


def export_tracking_report(
    browser: BrowserManager,
    settings: Settings,
    school_year: str,
) -> Path:
    """Export a Dinantia tracking report for the selected school year."""
    logger.info(
        "Starting Dinantia tracking export workflow for school year %s",
        school_year,
    )

    authenticated_page = open_authenticated_dinantia_page(
        browser,
        settings,
    )

    try:
        tracking_page = DinantiaTrackingPage(
            authenticated_page,
        )

        tracking_page.open()
        tracking_page.select_school_year(
            school_year,
        )
        tracking_page.open_detail()

        detail_page = DinantiaDetailPage(
            authenticated_page,
        )

        downloaded_file = detail_page.export_report(
            settings.download_dir,
        )

        logger.info(
            "Dinantia tracking export workflow completed: %s",
            downloaded_file,
        )

        return downloaded_file

    finally:
        if not authenticated_page.is_closed():
            authenticated_page.close()
