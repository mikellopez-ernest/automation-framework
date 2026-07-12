from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from automation.config import Settings, get_settings


def get_app_settings() -> Settings:
    """Return application settings."""
    return get_settings()


SettingsDependency = Annotated[
    Settings,
    Depends(get_app_settings),
]
