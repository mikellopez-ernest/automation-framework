from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends

from automation.api.locks import automation_lock
from automation.api.services import TrackingService
from automation.config import Settings, get_settings


def get_app_settings() -> Settings:
    """Return application settings."""
    return get_settings()


SettingsDependency = Annotated[
    Settings,
    Depends(get_app_settings),
]


def get_tracking_service(
    settings: SettingsDependency,
) -> TrackingService:
    """Return the Dinantia tracking application service."""
    return TrackingService(
        settings,
    )


TrackingServiceDependency = Annotated[
    TrackingService,
    Depends(get_tracking_service),
]


def acquire_automation_lock() -> Iterator[None]:
    """Prevent simultaneous browser automation executions."""
    with automation_lock.acquire():
        yield


AutomationLockDependency = Annotated[
    None,
    Depends(acquire_automation_lock),
]
