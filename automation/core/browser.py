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
    def __init__(
        self,
        settings: BrowserSettings,
        download_dir: Path,
        storage_state_path: Path | None = None,
    ) -> None:
        self._settings = settings
        self._download_dir = download_dir
        self._storage_state_path = storage_state_path

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

        self._storage_state_loaded = False

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

    @property
    def storage_state_loaded(self) -> bool:
        """Return whether a saved browser state was loaded."""
        return self._storage_state_loaded

    def start(self) -> None:
        if self._playwright is not None:
            return

        try:
            self._download_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._playwright = sync_playwright().start()

            browser_type = getattr(
                self._playwright,
                self._settings.engine,
            )

            self._browser = browser_type.launch(
                headless=self._settings.headless,
                slow_mo=self._settings.slow_mo_ms,
            )

            self._context = self._create_context()

            self._context.set_default_timeout(self._settings.timeout_ms)

            logger.info(
                "Browser started: engine=%s, headless=%s, storage_state=%s",
                self._settings.engine,
                self._settings.headless,
                self._storage_state_loaded,
            )

        except Exception as exc:
            self.close()
            raise BrowserError("Unable to start the browser") from exc

    def new_page(self) -> Page:
        if self._context is None:
            raise BrowserError("Browser manager has not been started")

        return self._context.new_page()

    def save_storage_state(
        self,
        path: Path | None = None,
    ) -> Path:
        """Save cookies and browser storage to disk."""
        if self._context is None:
            raise BrowserError("Browser manager has not been started")

        destination = path or self._storage_state_path

        if destination is None:
            raise BrowserError("No storage state path has been configured")

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._context.storage_state(path=str(destination))

        logger.info(
            "Browser storage state saved: %s",
            destination,
        )

        return destination

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

    def _create_context(self) -> BrowserContext:
        if self._browser is None:
            raise BrowserError("Browser has not been started")

        if self._storage_state_path is not None and self._storage_state_path.is_file():
            logger.info(
                "Loading browser storage state: %s",
                self._storage_state_path,
            )

            try:
                context = self._browser.new_context(
                    accept_downloads=True,
                    storage_state=str(self._storage_state_path),
                )

                self._storage_state_loaded = True
                return context

            except Exception:
                logger.warning(
                    "Unable to load browser storage state. "
                    "Starting with a clean context.",
                    exc_info=True,
                )

        self._storage_state_loaded = False

        return self._browser.new_context(accept_downloads=True)
