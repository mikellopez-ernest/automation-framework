from __future__ import annotations

import logging

from automation.config.loader import get_settings
from automation.core.browser import BrowserManager
from automation.core.logger import configure_logging
from automation.portals.dinantia import DinantiaHomePage


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    logger = logging.getLogger(__name__)
    logger.info("Starting Dinantia login-page test")

    with BrowserManager(
        settings.browser,
        settings.download_dir,
    ) as browser:
        home_browser_page = browser.new_page()
        home_page = DinantiaHomePage(home_browser_page)

        home_page.open()
        home_page.reject_cookie_notice()

        login_page = home_page.open_login_page()

        logger.info(
            "Login page title: %s",
            login_page.title(),
        )

        login_page.close()

    logger.info("Dinantia login-page test completed")


if __name__ == "__main__":
    main()
