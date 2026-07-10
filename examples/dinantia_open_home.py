import logging

from automation.config.loader import get_settings
from automation.core.browser import BrowserManager
from automation.core.logger import configure_logging
from automation.portals.dinantia.constants import DINANTIA_HOME_URL

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    logger.info("Opening Dinantia home page")

    with BrowserManager(settings.browser, settings.download_dir) as browser:
        page = browser.new_page()
        page.goto(DINANTIA_HOME_URL, wait_until="domcontentloaded")
        logger.info("Dinantia loaded: %s", page.title())


if __name__ == "__main__":
    main()
