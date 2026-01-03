from __future__ import annotations

from .domain import AssignmentContext


def calculate_occupied_slots(ctx: AssignmentContext, day: str) -> int:
    occupied = 0
    for var in ["V1", "V2", "V3", "V4"]:
        if day in ctx.slots[var]:
            for start, end in ctx.slots[var][day]:
                occupied += (end + 1 - start)
    return occupied


def assign_slots_in_blocks(ctx: AssignmentContext, day: str, needed_slots: int) -> int:
    possible_blocks = [18, 36, 54, 72]  # 1.5h, 3h, 4.5h, 6h (5-min slots)
    day_slots = ctx.daily_domains[day]
    assigned_slots = 0
    current_block_start = None
    current_block_count = 0

    for slot in day_slots:
        if assigned_slots >= needed_slots:
            break

        if slot in ctx.general_domain_reduced:
            if current_block_start is None:
                current_block_start = slot
            current_block_count += 1

            if (
                current_block_count in possible_blocks
                and assigned_slots + current_block_count <= needed_slots
            ):
                for s in range(
                        current_block_start,
                        current_block_start + current_block_count,
                    ):
                    ctx.schedule[s] = ctx.variables["V10"]
                    ctx.remove_slot(s)
                assigned_slots += current_block_count
                current_block_start = None
                current_block_count = 0
        else:
            current_block_start = None
            current_block_count = 0

    return assigned_slots


def assign_weekend_slots_limited(
    ctx: AssignmentContext,
    day: str,
    possible_blocks: list[int],
    max_slots_per_day: int,
) -> int:
    day_start_slot = ctx.daily_domains[day][0]
    assigned_slots = 0
    current_block_start = None
    current_block_count = 0

    for slot in range(day_start_slot, day_start_slot + 288):
        if assigned_slots >= max_slots_per_day:
            break
        if slot in ctx.general_domain_reduced:
            if current_block_start is None:
                current_block_start = slot
            current_block_count += 1

            if (
                current_block_count in possible_blocks
                and assigned_slots + current_block_count <= max_slots_per_day
            ):
                for s in range(
                        current_block_start,
                        current_block_start + current_block_count,
                    ):
                    ctx.schedule[s] = ctx.variables["V10"]
                    ctx.remove_slot(s)
                assigned_slots += current_block_count
                current_block_start = None
                current_block_count = 0
        else:
            current_block_start = None
            current_block_count = 0

    return assigned_slots


def assign_workout_slots(ctx: AssignmentContext) -> None:
    possible_blocks = 9  # 45 minutes
    days_assigned = 0

    for _day, intervals in ctx.slots["V11"].items():
        if days_assigned >= 3:
            break

        for start_range, end_range in intervals:
            current_block_start = None
            current_block_count = 0

            for slot in range(start_range, end_range + 1):
                if slot in ctx.general_domain_reduced:
                    if current_block_start is None:
                        current_block_start = slot
                    current_block_count += 1

                    if current_block_count == possible_blocks:
                        for s in range(
                        current_block_start,
                        current_block_start + current_block_count,
                    ):
                            ctx.schedule[s] = ctx.variables["V11"]
                            ctx.remove_slot(s)
                        days_assigned += 1
                        break
                else:
                    current_block_start = None
                    current_block_count = 0

            if days_assigned >= 3:
                break


def assign_shopping_slots(ctx: AssignmentContext) -> None:
    possible_blocks = 12  # 1 hour
    assigned = False

    for _day, intervals in ctx.slots["V12"].items():
        for start_range, end_range in intervals:
            current_block_start = None
            current_block_count = 0

            for slot in range(start_range, end_range + 1):
                if slot in ctx.general_domain_reduced and not assigned:
                    if current_block_start is None:
                        current_block_start = slot
                    current_block_count += 1

                    if current_block_count == possible_blocks:
                        for s in range(
                        current_block_start,
                        current_block_start + current_block_count,
                    ):
                            ctx.schedule[s] = ctx.variables["V12"]
                            ctx.remove_slot(s)
                        assigned = True
                        break
                else:
                    current_block_start = None
                    current_block_count = 0

            if assigned:
                break

        if assigned:
            break


def assign_cleaning_slots(ctx: AssignmentContext) -> None:
    possible_blocks = 12  # 1 hour
    assigned = False

    for _day, intervals in ctx.slots["V13"].items():
        for start_range, end_range in intervals:
            current_block_start = None
            current_block_count = 0

            for slot in range(start_range, end_range + 1):
                if slot in ctx.general_domain_reduced and not assigned:
                    if current_block_start is None:
                        current_block_start = slot
                    current_block_count += 1

                    if current_block_count == possible_blocks:
                        for s in range(
                        current_block_start,
                        current_block_start + current_block_count,
                    ):
                            ctx.schedule[s] = ctx.variables["V13"]
                            ctx.remove_slot(s)
                        assigned = True
                        break
                else:
                    current_block_start = None
                    current_block_count = 0

            if assigned:
                break

        if assigned:
            break


def assign_personal_time_slots(ctx: AssignmentContext) -> None:
    for _day, intervals in ctx.slots["V14"].items():
        for start_range, end_range in intervals:
            for slot in range(start_range, end_range + 1):
                if slot in ctx.general_domain_reduced:
                    ctx.schedule[slot] = ctx.variables["V14"]
                    ctx.remove_slot(slot)
