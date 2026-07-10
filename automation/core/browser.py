from __future__ import annotations

import logging
from pathlib import Path
from types import TracebackType

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from automation.config.settings import BrowserSettings

from .exceptions import BrowserError

logger = logging.getLogger(__name__)


class BrowserManager:
    def __init__(self, settings: BrowserSettings, download_dir: Path) -> None:
        self._settings = settings
        self._download_dir = download_dir
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    def __enter__(self) -> BrowserManager:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def start(self) -> None:
        if self._playwright is not None:
            return

        try:
            self._download_dir.mkdir(parents=True, exist_ok=True)
            self._playwright = sync_playwright().start()
            browser_type = getattr(self._playwright, self._settings.engine)
            self._browser = browser_type.launch(
                headless=self._settings.headless,
                slow_mo=self._settings.slow_mo_ms,
            )
            self._context = self._browser.new_context(accept_downloads=True)
            self._context.set_default_timeout(self._settings.timeout_ms)
            logger.info(
                "Browser started: engine=%s, headless=%s",
                self._settings.engine,
                self._settings.headless,
            )
        except Exception as exc:
            self.close()
            raise BrowserError("Unable to start the browser") from exc

    def new_page(self) -> Page:
        if self._context is None:
            raise BrowserError("Browser manager has not been started")
        return self._context.new_page()

    def close(self) -> None:
        if self._context is not None:
            self._context.close()
            self._context = None
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None
        logger.info("Browser closed")
