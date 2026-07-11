from __future__ import annotations

import pytest

from automation.models import TrackingFilters


def test_tracking_filters_normalizes_school_year() -> None:
    filters = TrackingFilters(
        school_year=" 2025-26 ",
    )

    assert filters.school_year == "2025-26"


def test_tracking_filters_rejects_empty_school_year() -> None:
    with pytest.raises(
        ValueError,
        match="school_year cannot be empty",
    ):
        TrackingFilters(
            school_year="   ",
        )
