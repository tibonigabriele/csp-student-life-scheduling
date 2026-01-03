from __future__ import annotations

import re

from csp_student_life.schedule import build_schedule, schedule_to_jsonable

_TIME_RE = re.compile(r"^\d{2}:\d{2}$")


def test_build_schedule_has_expected_length() -> None:
    flat = build_schedule()
    assert len(flat) == 2016
    assert all(isinstance(x, str) and x for x in flat)


def test_json_shape_and_time_format() -> None:
    flat = build_schedule()
    payload = schedule_to_jsonable(flat)

    assert set(payload.keys()) == {
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    }

    for _day, items in payload.items():
        assert isinstance(items, list)
        assert len(items) > 0
        for it in items:
            assert set(it.keys()) == {"start", "end", "activity"}
            assert _TIME_RE.match(it["start"])
            assert _TIME_RE.match(it["end"])
            assert isinstance(it["activity"], str) and it["activity"]
