from __future__ import annotations

import logging

from automation.config.loader import get_settings
from automation.core.browser import BrowserManager
from automation.core.logger import configure_logging
from automation.portals.dinantia import (
    DinantiaDetailPage,
    DinantiaTrackingPage,
)
from automation.workflows.dinantia import open_authenticated_dinantia_page


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    logger = logging.getLogger(__name__)
    logger.info("Starting Dinantia tracking export test")

    with BrowserManager(
        settings.browser,
        settings.download_dir,
        storage_state_path=settings.dinantia_storage_state_path,
    ) as browser:
        authenticated_page = open_authenticated_dinantia_page(
            browser,
            settings,
        )

        tracking_page = DinantiaTrackingPage(
            authenticated_page,
        )

        tracking_page.open()
        tracking_page.select_school_year("2025-26")
        tracking_page.open_detail()

        detail_page = DinantiaDetailPage(
            authenticated_page,
        )

        downloaded_file = detail_page.export_report(
            settings.download_dir,
        )

        logger.info(
            "Downloaded report: %s",
            downloaded_file.resolve(),
        )

        authenticated_page.close()

    logger.info("Dinantia tracking export test completed")


if __name__ == "__main__":
    main()
