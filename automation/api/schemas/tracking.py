from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ExportTrackingRequest(BaseModel):
    """Request body for exporting a Dinantia tracking report."""

    school_year: str = Field(
        min_length=1,
        examples=["2025-26"],
        description="School year exactly as displayed by Dinantia.",
    )

    @field_validator("school_year")
    @classmethod
    def normalize_school_year(cls, value: str) -> str:
        """Normalize and validate the supplied school year."""
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("school_year cannot be empty")

        return normalized_value
