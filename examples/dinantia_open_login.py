from __future__ import annotations

import logging

from automation.config import get_settings
from automation.core import BrowserManager, configure_logging
from automation.portals.dinantia.home import DinantiaHomePage


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    logger = logging.getLogger(__name__)
    logger.info("Starting Dinantia login-page test")

    with BrowserManager(
        settings.browser,
        settings.download_dir,
    ) as browser:
        public_browser_page = browser.new_page()
        home_page = DinantiaHomePage(public_browser_page)

        home_page.open()
        home_page.reject_cookie_notice()

        login_browser_page = home_page.open_login_page()

        logger.info(
            "Login page title: %s",
            login_browser_page.title(),
        )

        login_browser_page.close()

    logger.info("Dinantia login-page test completed")


if __name__ == "__main__":
    main()
