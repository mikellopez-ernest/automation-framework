from __future__ import annotations

import logging

from automation.config.loader import get_settings
from automation.core.browser import BrowserManager
from automation.core.logger import configure_logging
from automation.workflows.dinantia import export_tracking_report


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    logger = logging.getLogger(__name__)
    logger.info("Starting Dinantia tracking export example")

    with BrowserManager(
        settings.browser,
        settings.download_dir,
        storage_state_path=settings.dinantia_storage_state_path,
    ) as browser:
        downloaded_file = export_tracking_report(
            browser,
            settings,
            "2025-26",
        )

        logger.info(
            "Downloaded report: %s",
            downloaded_file.resolve(),
        )

    logger.info("Dinantia tracking export example completed")


if __name__ == "__main__":
    main()
