from __future__ import annotations

from pathlib import Path

from automation.core.downloads import DownloadManager
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

        export_button = Elements.button(
            self.page,
            EXPORT_BUTTON_TEXT,
        )

        export_button.wait_for(
            state="visible",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        def trigger_export() -> None:
            export_button.click()

        try:
            destination = DownloadManager.download_with_retries(
                self.page,
                trigger_export,
                download_dir,
                logger=self.logger,
                max_attempts=MAX_EXPORT_ATTEMPTS,
                attempt_timeout_ms=DOWNLOAD_ATTEMPT_TIMEOUT_MS,
                retry_delay_ms=DOWNLOAD_RETRY_DELAY_MS,
            )
        except RuntimeError as exc:
            raise RuntimeError(
                "Dinantia did not generate the tracking report "
                f"after {MAX_EXPORT_ATTEMPTS} attempts"
            ) from exc

        self.logger.info(
            "Dinantia tracking report saved: %s",
            destination,
        )

        return destination
