from __future__ import annotations

import json
from typing import Any

from .data import DAILY_DOMAINS, SLOTS, VARIABLES, NSLOTS
from .domain import AssignmentContext, slot_to_time
from .heuristics import (
    assign_cleaning_slots,
    assign_personal_time_slots,
    assign_shopping_slots,
    assign_slots_in_blocks,
    assign_weekend_slots_limited,
    assign_workout_slots,
    calculate_occupied_slots,
)


def _assign_fixed(ctx: AssignmentContext, var_ids: list[str]) -> None:
    for var in var_ids:
        for _day, intervals in ctx.slots[var].items():
            for start, end in intervals:
                for s in range(start, end + 1):
                    ctx.schedule[s] = ctx.variables[var]
                    ctx.remove_slot(s)


def _recompute_free_domain(ctx: AssignmentContext) -> None:
    ctx.general_domain_reduced[:] = [i for i, a in enumerate(ctx.schedule) if a is None]


def build_schedule() -> list[str]:
    schedule: list[str | None] = [None] * NSLOTS
    ctx = AssignmentContext(
        variables=VARIABLES,
        slots=SLOTS,
        daily_domains=DAILY_DOMAINS,
        schedule=schedule,
        general_domain_reduced=[],
        points_to_remove=[],
    )

    fixed = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9"]
    _assign_fixed(ctx, fixed)
    _recompute_free_domain(ctx)

    # Study time (V10), matching the notebook mapping derived from class occupancy:
    slots_needed_per_day: dict[str, int] = {}
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        occupied = calculate_occupied_slots(ctx, day)
        remaining = 288 - occupied
        if day == "Friday":
            needed = 72
        elif remaining >= 216:
            needed = 36
        else:
            needed = 18
        slots_needed_per_day[day] = needed

    for day, needed in slots_needed_per_day.items():
        assign_slots_in_blocks(ctx, day, needed)

    weekend_blocks = [18, 36]
    max_slots_daily = 36
    for day in ["Saturday", "Sunday"]:
        assign_weekend_slots_limited(ctx, day, weekend_blocks, max_slots_daily)

    assign_workout_slots(ctx)
    assign_shopping_slots(ctx)
    assign_cleaning_slots(ctx)
    assign_personal_time_slots(ctx)

    for i in range(NSLOTS):
        if ctx.schedule[i] is None:
            ctx.schedule[i] = "Free"

    return [a for a in ctx.schedule]  # type: ignore[misc]


def schedule_to_jsonable(flat_schedule: list[str]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {day: [] for day in DAILY_DOMAINS.keys()}

    for day, slots_range in DAILY_DOMAINS.items():
        current_activity = None
        activity_start = None

        for slot_index in slots_range:
            slot_activity = flat_schedule[slot_index]
            if slot_activity != current_activity:
                if current_activity is not None and activity_start is not None:
                    start_time = slot_to_time(activity_start, slots_range[0])
                    end_time = slot_to_time(slot_index - 1, slots_range[0], extra_minutes=5)
                    out[day].append({"start": start_time, "end": end_time, "activity": current_activity})
                current_activity = slot_activity
                activity_start = slot_index

        if current_activity is not None and activity_start is not None:
            start_time = slot_to_time(activity_start, slots_range[0])
            end_time = slot_to_time(slots_range[-1], slots_range[0], extra_minutes=5)
            out[day].append({"start": start_time, "end": end_time, "activity": current_activity})

    return out


def write_json(schedule_json: dict[str, Any], out_path: str, pretty: bool = True) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(schedule_json, f, indent=2, ensure_ascii=False)
        else:
            json.dump(schedule_json, f, separators=(",", ":"), ensure_ascii=False)
