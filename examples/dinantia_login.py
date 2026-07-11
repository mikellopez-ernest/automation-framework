from __future__ import annotations

import logging

from automation.config.loader import get_settings
from automation.core.browser import BrowserManager
from automation.core.logger import configure_logging
from automation.portals.dinantia import (
    DinantiaHomePage,
    DinantiaLoginPage,
)


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    logger = logging.getLogger(__name__)

    if not settings.dinantia_username:
        raise RuntimeError("AUTOMATION_DINANTIA_USERNAME is not configured in .env")

    if not settings.dinantia_password:
        raise RuntimeError("AUTOMATION_DINANTIA_PASSWORD is not configured in .env")

    logger.info("Starting Dinantia authentication test")

    with BrowserManager(
        settings.browser,
        settings.download_dir,
    ) as browser:
        public_browser_page = browser.new_page()
        home_page = DinantiaHomePage(public_browser_page)

        home_page.open()
        home_page.reject_cookie_notice()

        login_browser_page = home_page.open_login_page()
        login_page = DinantiaLoginPage(login_browser_page)

        login_page.authenticate(
            settings.dinantia_username,
            settings.dinantia_password,
        )

        logger.info(
            "Current authenticated URL: %s",
            login_browser_page.url,
        )

        login_browser_page.close()

    logger.info("Dinantia authentication test completed")


if __name__ == "__main__":
    main()
