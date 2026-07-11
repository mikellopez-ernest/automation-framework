from __future__ import annotations

import logging

from playwright.sync_api import Page

from automation.core.elements import Elements


from .constants import (
    COOKIE_REJECT_LINK_TEXT,
    DEFAULT_TIMEOUT_MS,
    DINANTIA_HOME_URL,
    DINANTIA_LOGIN_URL_PREFIX,
    SIGN_IN_LINK_TEXT,
)

logger = logging.getLogger(__name__)


class DinantiaHomePage:
    """Dinantia public home page."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        """Open the Dinantia public website."""
        logger.info("Opening Dinantia home page")

        self.page.goto(
            DINANTIA_HOME_URL,
            wait_until="domcontentloaded",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        logger.info("Dinantia home page loaded")

    def reject_cookie_notice(self) -> None:
        """Reject the cookie or privacy notice when it is visible."""
        reject_link = Elements.link(
            self.page,
            COOKIE_REJECT_LINK_TEXT,
        )

        if reject_link.is_visible():
            logger.info("Rejecting Dinantia notice")
            reject_link.click()
        else:
            logger.info("Dinantia notice is not visible")

    def open_login_page(self) -> Page:
        """Open the Dinantia login page in the new browser tab."""
        sign_in_link = Elements.link(
            self.page,
            SIGN_IN_LINK_TEXT,
        )

        sign_in_link.wait_for(
            state="visible",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        logger.info("Opening Dinantia login page")

        with self.page.expect_popup(
            timeout=DEFAULT_TIMEOUT_MS,
        ) as popup_info:
            sign_in_link.click()

        login_page = popup_info.value

        login_page.wait_for_load_state(
            "domcontentloaded",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        login_page.wait_for_url(
            lambda url: url.startswith(DINANTIA_LOGIN_URL_PREFIX),
            timeout=DEFAULT_TIMEOUT_MS,
        )

        logger.info(
            "Dinantia login page opened: %s",
            login_page.url,
        )

        return login_page
