from __future__ import annotations

import pytest
from pydantic import ValidationError as PydanticValidationError

from automation.api.schemas import ExportTrackingRequest


def test_export_tracking_request_normalizes_school_year() -> None:
    request = ExportTrackingRequest(
        school_year=" 2025-26 ",
    )

    assert request.school_year == "2025-26"


def test_export_tracking_request_rejects_empty_school_year() -> None:
    with pytest.raises(PydanticValidationError):
        ExportTrackingRequest(
            school_year="   ",
        )
