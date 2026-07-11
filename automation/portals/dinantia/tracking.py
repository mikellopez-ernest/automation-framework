from __future__ import annotations

from automation.core.elements import Elements
from automation.core.page import BasePage

from .constants import (
    DEFAULT_TIMEOUT_MS,
    TRACKING_PAGE_URL_FRAGMENT,
)

TRACKING_MENU_TEXT = "Seguiment"


class DinantiaTrackingPage(BasePage):
    """Dinantia tracking page."""

    def open(self) -> None:
        """Open the tracking section."""

        self.logger.info("Opening tracking page")

        tracking_menu = Elements.role(
            self.page,
            "treeitem",
            TRACKING_MENU_TEXT,
        )

        tracking_menu.click()

        self.page.wait_for_url(
            lambda url: TRACKING_PAGE_URL_FRAGMENT in url,
            timeout=DEFAULT_TIMEOUT_MS,
        )

        self.logger.info(
            "Tracking page opened: %s",
            self.page.url,
        )
