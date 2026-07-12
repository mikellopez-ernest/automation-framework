from __future__ import annotations

import threading
from collections.abc import Iterator
from contextlib import contextmanager

from automation.core.exceptions import AutomationError


class AutomationBusyError(AutomationError):
    """Raised when another automation is already running."""


class AutomationLock:
    """Serialize browser automation executions within the API process."""

    def __init__(self) -> None:
        self._lock = threading.Lock()

    @contextmanager
    def acquire(self) -> Iterator[None]:
        """Acquire the automation lock without waiting."""
        acquired = self._lock.acquire(
            blocking=False,
        )

        if not acquired:
            raise AutomationBusyError("Another automation is currently running")

        try:
            yield
        finally:
            self._lock.release()


automation_lock = AutomationLock()
