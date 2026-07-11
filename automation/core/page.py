from __future__ import annotations

import logging

from playwright.sync_api import Page


class BasePage:
    """Base class for all portal pages."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)
