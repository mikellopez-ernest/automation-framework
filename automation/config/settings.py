from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BrowserEngine = Literal["chromium", "firefox", "webkit"]


class BrowserSettings(BaseModel):
    engine: BrowserEngine = "firefox"
    headless: bool = False
    timeout_ms: int = Field(default=30_000, ge=1_000)
    slow_mo_ms: int = Field(default=0, ge=0)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AUTOMATION_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    browser_engine: BrowserEngine = "firefox"
    browser_headless: bool = False
    browser_timeout_ms: int = 30_000
    browser_slow_mo_ms: int = 0

    log_level: str = "INFO"
    download_dir: Path = Path("downloads")

    api_token: str | None = None

    dinantia_username: str | None = None
    dinantia_password: str | None = None
    dinantia_storage_state_path: Path = Path(".playwright/auth/dinantia.json")

    @property
    def browser(self) -> BrowserSettings:
        return BrowserSettings(
            engine=self.browser_engine,
            headless=self.browser_headless,
            timeout_ms=self.browser_timeout_ms,
            slow_mo_ms=self.browser_slow_mo_ms,
        )
