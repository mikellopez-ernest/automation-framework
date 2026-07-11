from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrackingFilters:
    """Filters used to export Dinantia tracking data."""

    school_year: str

    def __post_init__(self) -> None:
        normalized_school_year = self.school_year.strip()

        if not normalized_school_year:
            raise ValueError("school_year cannot be empty")

        object.__setattr__(
            self,
            "school_year",
            normalized_school_year,
        )
