class AutomationError(Exception):
    """Base exception for the automation framework."""


class BrowserError(AutomationError):
    """Raised when the browser cannot be started or used."""
