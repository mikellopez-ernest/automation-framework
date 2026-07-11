from __future__ import annotations

import logging
import time

from playwright.sync_api import Page

from automation.config.loader import get_settings
from automation.core.browser import BrowserManager
from automation.core.logger import configure_logging
from automation.portals.dinantia import (
    DinantiaHomePage,
    DinantiaLoginPage,
)
from automation.portals.dinantia.constants import (
    DEFAULT_TIMEOUT_MS,
    DINANTIA_INBOX_URL,
)

AUTHENTICATED_TRACKING_SELECTOR = 'a[href="/attitude/"][role="treeitem"]'

LOGIN_PASSWORD_SELECTOR = 'input[type="password"]'


def has_valid_session(
    page: Page,
    timeout_ms: int = DEFAULT_TIMEOUT_MS,
) -> bool:
    """Return whether the current browser session is authenticated."""

    deadline = time.monotonic() + timeout_ms / 1000

    tracking_link = page.locator(AUTHENTICATED_TRACKING_SELECTOR).first

    password_input = page.locator(LOGIN_PASSWORD_SELECTOR).first

    while time.monotonic() < deadline:
        if tracking_link.count() > 0:
            return True

        if password_input.count() > 0 and password_input.is_visible():
            return False

        page.wait_for_timeout(250)

    return False


def require_credentials(
    username: str | None,
    password: str | None,
) -> tuple[str, str]:
    if not username:
        raise RuntimeError("AUTOMATION_DINANTIA_USERNAME is not configured.")

    if not password:
        raise RuntimeError("AUTOMATION_DINANTIA_PASSWORD is not configured.")

    return username, password


def main() -> None:
    settings = get_settings()

    configure_logging(
        settings.log_level,
    )

    logger = logging.getLogger(__name__)

    logger.info("Starting Dinantia authentication test")

    with BrowserManager(
        settings.browser,
        settings.download_dir,
        storage_state_path=settings.dinantia_storage_state_path,
    ) as browser:
        if browser.storage_state_loaded:
            page = browser.new_page()

            logger.info("Checking saved Dinantia session")

            page.goto(
                DINANTIA_INBOX_URL,
                wait_until="domcontentloaded",
                timeout=DEFAULT_TIMEOUT_MS,
            )

            if has_valid_session(page):
                logger.info("Saved Dinantia session is valid.")

                page.close()
                return

            logger.info("Saved Dinantia session is expired.")

            page.close()

        username, password = require_credentials(
            settings.dinantia_username,
            settings.dinantia_password,
        )

        public_page = browser.new_page()

        home = DinantiaHomePage(
            public_page,
        )

        home.open()
        home.reject_cookie_notice()

        login_browser_page = home.open_login_page()

        def save_dinantia_session() -> None:
            browser.save_storage_state()

        login = DinantiaLoginPage(
            login_browser_page,
            save_session=save_dinantia_session,
        )

        login.authenticate(
            username,
            password,
        )

        logger.info(
            "Authenticated URL: %s",
            login_browser_page.url,
        )

        login_browser_page.close()
        public_page.close()

    logger.info("Dinantia authentication test completed")


if __name__ == "__main__":
    main()
