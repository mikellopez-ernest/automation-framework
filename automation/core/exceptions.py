from __future__ import annotations


class AutomationError(Exception):
    """Base exception for the automation framework."""


#
# Infrastructure
#
class BrowserError(AutomationError):
    """Raised when the browser cannot be started or used."""


class DownloadError(AutomationError):
    """Raised when a browser download cannot be completed."""


class ValidationError(AutomationError):
    """Raised when supplied data is invalid."""


#
# Authentication
#
class AuthenticationError(AutomationError):
    """Raised when authentication cannot be completed."""


class SessionError(AuthenticationError):
    """Raised when a stored authenticated session is invalid."""


#
# Portals
#
class PortalError(AutomationError):
    """Base exception for portal-specific errors."""


class DinantiaError(PortalError):
    """Base exception for Dinantia-specific errors."""


class DinantiaTrackingError(DinantiaError):
    """Raised when a tracking operation fails."""


class DinantiaExportError(DinantiaTrackingError):
    """Raised when exporting a tracking report fails."""
