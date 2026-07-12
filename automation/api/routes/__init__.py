from .health import router as health_router
from .root import router as root_router
from .v1 import dinantia_router

__all__ = [
    "dinantia_router",
    "health_router",
    "root_router",
]
