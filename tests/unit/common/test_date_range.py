from datetime import datetime, UTC, timedelta

import pytest
from pydantic import ValidationError

from src.schemes.common import DatetimeRange


@pytest.mark.parametrize(
    "date_from, date_to, should_raise",
    [
        (datetime.now(UTC) - timedelta(days=5), datetime.now(UTC), False),  # ✅ Valid range
        (None, None, False),  # ✅ Both None (valid)
        (datetime.now(UTC), None, True),  # ❌ Only date_from specified
        (None, datetime.now(UTC), True),  # ❌ Only date_to specified
        (datetime.now(UTC), datetime.now(UTC) - timedelta(days=1), True),  # ❌ date_to < date_from
        (datetime.now(UTC), datetime.now(UTC), False),  # ✅ Edge case: date_from == date_to
    ],
)
def test_datetime_range_validation(date_from, date_to, should_raise):
    """Test validation of DatetimeRange with different date combinations."""
    if should_raise:
        with pytest.raises(ValidationError):
            DatetimeRange(date_from=date_from, date_to=date_to)
    else:
        instance = DatetimeRange(date_from=date_from, date_to=date_to)
        assert instance.date_from == date_from
        assert instance.date_to == date_to