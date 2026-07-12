from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class RootResponse(BaseModel):
    """API root response."""

    service: str
    version: str
    status: Literal["running"]


class HealthResponse(BaseModel):
    """Health-check response."""

    status: Literal["ok"]
