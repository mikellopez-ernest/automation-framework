from __future__ import annotations

from pathlib import Path

from playwright.sync_api import (
    Page,
)
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)

from automation.core.elements import Elements
from automation.core.page import BasePage

from .constants import DEFAULT_TIMEOUT_MS

EXPORT_BUTTON_TEXT = "Exportar"

DOWNLOAD_ATTEMPT_TIMEOUT_MS = 30_000
DOWNLOAD_RETRY_DELAY_MS = 2_000
MAX_EXPORT_ATTEMPTS = 3


class DinantiaDetailPage(BasePage):
    """Dinantia detailed tracking page."""

    def export_report(
        self,
        download_dir: Path,
    ) -> Path:
        """Export and save the detailed tracking report."""
        self.logger.info("Exporting Dinantia tracking report")

        download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        export_button = Elements.button(
            self.page,
            EXPORT_BUTTON_TEXT,
        )

        export_button.wait_for(
            state="visible",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        for attempt in range(1, MAX_EXPORT_ATTEMPTS + 1):
            self.logger.info(
                "Export attempt %d of %d",
                attempt,
                MAX_EXPORT_ATTEMPTS,
            )

            pages_before_export = set(self.page.context.pages)

            try:
                with self.page.expect_download(
                    timeout=DOWNLOAD_ATTEMPT_TIMEOUT_MS,
                ) as download_info:
                    export_button.click()

                download = download_info.value

                destination = self._build_destination(
                    download_dir,
                    download.suggested_filename,
                )

                download.save_as(destination)

                self._close_export_pages(
                    pages_before_export,
                )

                self.logger.info(
                    "Dinantia tracking report saved: %s",
                    destination,
                )

                return destination

            except PlaywrightTimeoutError:
                self.logger.warning(
                    "No download was received during export attempt %d",
                    attempt,
                )

                self._log_new_pages(
                    pages_before_export,
                )

                self._close_export_pages(
                    pages_before_export,
                )

                if attempt >= MAX_EXPORT_ATTEMPTS:
                    break

                self.page.bring_to_front()

                self.logger.info(
                    "Retrying export in %.1f seconds",
                    DOWNLOAD_RETRY_DELAY_MS / 1_000,
                )

                self.page.wait_for_timeout(
                    DOWNLOAD_RETRY_DELAY_MS,
                )

                export_button.wait_for(
                    state="visible",
                    timeout=DEFAULT_TIMEOUT_MS,
                )

        raise RuntimeError(
            "Dinantia did not generate the tracking report "
            f"after {MAX_EXPORT_ATTEMPTS} attempts"
        )

    def _log_new_pages(
        self,
        pages_before_export: set[Page],
    ) -> None:
        """Log temporary pages opened during a failed export."""
        for page in self.page.context.pages:
            if page in pages_before_export or page.is_closed():
                continue

            try:
                self.logger.warning(
                    "Export opened temporary page: url=%s title=%s",
                    page.url,
                    page.title(),
                )
            except Exception:
                self.logger.warning(
                    "Export opened a temporary page that could not be inspected"
                )

    def _close_export_pages(
        self,
        pages_before_export: set[Page],
    ) -> None:
        """Close any temporary page opened during the export."""
        for page in self.page.context.pages:
            if page not in pages_before_export and not page.is_closed():
                page.close()

    @staticmethod
    def _build_destination(
        download_dir: Path,
        suggested_filename: str,
    ) -> Path:
        """Return a non-conflicting destination path."""
        destination = download_dir / suggested_filename

        if not destination.exists():
            return destination

        stem = destination.stem
        suffix = destination.suffix
        counter = 1

        while True:
            candidate = download_dir / (f"{stem}_{counter}{suffix}")

            if not candidate.exists():
                return candidate

            counter += 1
