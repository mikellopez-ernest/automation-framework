from __future__ import annotations

import logging
import time

from playwright.sync_api import Page

from automation.config.settings import Settings
from automation.core.browser import BrowserManager
from automation.core.exceptions import AuthenticationError
from automation.portals.dinantia.constants import (
    DEFAULT_TIMEOUT_MS,
    DINANTIA_INBOX_URL,
)
from automation.portals.dinantia.home import DinantiaHomePage
from automation.portals.dinantia.login import DinantiaLoginPage

logger = logging.getLogger(__name__)

AUTHENTICATED_TRACKING_SELECTOR = 'a[href="/attitude/"][role="treeitem"]'
LOGIN_PASSWORD_SELECTOR = 'input[type="password"]'


def open_authenticated_dinantia_page(
    browser: BrowserManager,
    settings: Settings,
) -> Page:
    """Return a Dinantia page with a valid authenticated session."""
    if browser.storage_state_loaded:
        session_page: Page = browser.new_page()

        logger.info("Checking saved Dinantia session")

        session_page.goto(
            DINANTIA_INBOX_URL,
            wait_until="domcontentloaded",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        if _has_valid_session(session_page):
            logger.info(
                "Saved Dinantia session is valid: %s",
                session_page.url,
            )
            return session_page

        logger.info("Saved Dinantia session is expired or invalid")
        session_page.close()

    username, password = _require_credentials(settings)

    public_page: Page = browser.new_page()
    home_page = DinantiaHomePage(public_page)

    home_page.open()
    home_page.reject_cookie_notice()

    login_browser_page: Page = home_page.open_login_page()

    def save_dinantia_session() -> None:
        browser.save_storage_state()

    login_page = DinantiaLoginPage(
        login_browser_page,
        save_session=save_dinantia_session,
    )

    login_page.authenticate(
        username,
        password,
    )

    public_page.close()

    return login_browser_page


def _has_valid_session(
    page: Page,
    timeout_ms: int = DEFAULT_TIMEOUT_MS,
) -> bool:
    """Return whether Dinantia displays an authenticated interface."""
    deadline = time.monotonic() + timeout_ms / 1_000

    tracking_link = page.locator(AUTHENTICATED_TRACKING_SELECTOR).first

    password_input = page.locator(LOGIN_PASSWORD_SELECTOR).first

    while time.monotonic() < deadline:
        if tracking_link.count() > 0:
            return True

        if password_input.count() > 0 and password_input.is_visible():
            return False

        page.wait_for_timeout(250)

    return False


def _require_credentials(
    settings: Settings,
) -> tuple[str, str]:
    """Return configured credentials or raise a clear error."""
    if not settings.dinantia_username:
        raise AuthenticationError(
            "AUTOMATION_DINANTIA_USERNAME is not configured in .env"
        )

    if not settings.dinantia_password:
        raise AuthenticationError(
            "AUTOMATION_DINANTIA_PASSWORD is not configured in .env"
        )

    return (
        settings.dinantia_username,
        settings.dinantia_password,
    )
