from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path

from playwright.sync_api import (
    Page,
)
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)


class DownloadManager:
    """Reusable Playwright download infrastructure."""

    @staticmethod
    def download_with_retries(
        page: Page,
        trigger: Callable[[], None],
        download_dir: Path,
        *,
        logger: logging.Logger,
        max_attempts: int = 3,
        attempt_timeout_ms: int = 30_000,
        retry_delay_ms: int = 2_000,
    ) -> Path:
        """Trigger and save a download, retrying failed attempts."""
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        for attempt in range(1, max_attempts + 1):
            logger.info(
                "Download attempt %d of %d",
                attempt,
                max_attempts,
            )

            pages_before_download = set(page.context.pages)

            try:
                with page.expect_download(
                    timeout=attempt_timeout_ms,
                ) as download_info:
                    trigger()

                download = download_info.value

                destination = DownloadManager.build_destination(
                    download_dir,
                    download.suggested_filename,
                )

                download.save_as(destination)

                DownloadManager.close_new_pages(
                    page,
                    pages_before_download,
                )

                logger.info(
                    "Download saved successfully: %s",
                    destination,
                )

                return destination

            except PlaywrightTimeoutError:
                logger.warning(
                    "No download was received during attempt %d",
                    attempt,
                )

                DownloadManager.log_new_pages(
                    page,
                    pages_before_download,
                    logger,
                )

                DownloadManager.close_new_pages(
                    page,
                    pages_before_download,
                )

                if attempt >= max_attempts:
                    break

                page.bring_to_front()

                logger.info(
                    "Retrying download in %.1f seconds",
                    retry_delay_ms / 1_000,
                )

                page.wait_for_timeout(
                    retry_delay_ms,
                )

        raise RuntimeError(f"No download was received after {max_attempts} attempts")

    @staticmethod
    def build_destination(
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

    @staticmethod
    def log_new_pages(
        page: Page,
        pages_before_download: set[Page],
        logger: logging.Logger,
    ) -> None:
        """Log temporary pages opened during a failed download."""
        for opened_page in page.context.pages:
            if opened_page in pages_before_download or opened_page.is_closed():
                continue

            try:
                logger.warning(
                    "Download opened temporary page: url=%s title=%s",
                    opened_page.url,
                    opened_page.title(),
                )
            except Exception:
                logger.warning(
                    "Download opened a temporary page that could not be inspected"
                )

    @staticmethod
    def close_new_pages(
        page: Page,
        pages_before_download: set[Page],
    ) -> None:
        """Close temporary pages opened during a download attempt."""
        for opened_page in page.context.pages:
            if opened_page not in pages_before_download and not opened_page.is_closed():
                opened_page.close()
