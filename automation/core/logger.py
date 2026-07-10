import logging

from rich.logging import RichHandler

_LOG_FORMAT = "%(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level.upper(),
        format=_LOG_FORMAT,
        datefmt=_DATE_FORMAT,
        handlers=[RichHandler(rich_tracebacks=True, markup=False)],
        force=True,
    )
