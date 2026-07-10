from automation.config.settings import Settings


def test_default_settings() -> None:
    settings = Settings(_env_file=None)

    assert settings.browser.engine == "firefox"
    assert settings.browser.headless is False
    assert settings.download_dir.name == "downloads"
