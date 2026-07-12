from __future__ import annotations

from collections.abc import Callable

from playwright.sync_api import (
    Page,
)
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)

from automation.core.elements import Elements
from automation.core.exceptions import AuthenticationError
from automation.core.page import BasePage

from .constants import DEFAULT_TIMEOUT_MS

EMAIL_INPUT_SELECTOR = 'input[type="email"]'
PASSWORD_INPUT_SELECTOR = 'input[type="password"]'
SUBMIT_BUTTON_SELECTOR = 'button[type="submit"]'
LOGIN_URL_FRAGMENT = "/login"


class DinantiaLoginPage(BasePage):
    """Dinantia login page."""

    def __init__(
        self,
        page: Page,
        save_session: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(page)
        self._save_session = save_session

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> None:
        """Authenticate a Dinantia user."""
        self.logger.info("Authenticating Dinantia user")

        self.page.wait_for_load_state(
            "networkidle",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        password_input = Elements.locator(
            self.page,
            PASSWORD_INPUT_SELECTOR,
        ).first

        password_input.wait_for(
            state="attached",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        login_container = password_input.locator(
            "xpath=ancestor::*[.//button[@type='submit']][1]"
        )

        email_input = login_container.locator(EMAIL_INPUT_SELECTOR).first

        login_button = login_container.locator(SUBMIT_BUTTON_SELECTOR).first

        email_input.wait_for(
            state="attached",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        login_button.wait_for(
            state="attached",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        self.logger.info(
            "Login elements found: container=%d email=%d password=%d submit=%d",
            login_container.count(),
            email_input.count(),
            password_input.count(),
            login_button.count(),
        )

        email_input.fill(
            username,
            force=True,
        )

        password_input.fill(
            password,
            force=True,
        )

        self.logger.info("Login credentials filled")

        login_button.click(
            force=True,
        )

        try:
            self.page.wait_for_url(
                lambda url: LOGIN_URL_FRAGMENT not in url,
                timeout=DEFAULT_TIMEOUT_MS,
            )
        except PlaywrightTimeoutError as exc:
            raise AuthenticationError(
                "Dinantia authentication did not complete successfully"
            ) from exc

        self.logger.info(
            "Dinantia authentication completed: %s",
            self.page.url,
        )

        if self._save_session is not None:
            self.logger.info("Persisting authenticated session")
            self._save_session()
