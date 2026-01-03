from __future__ import annotations

from dataclasses import dataclass


def slot_to_time(slot: int, day_start_slot: int, extra_minutes: int = 0) -> str:
    """Convert a global slot index into a HH:MM string relative to the given day start slot.

    The project uses 5-minute slots, with each day spanning 288 slots.
    """
    corrected_slot = slot - day_start_slot
    minutes = corrected_slot * 5 + extra_minutes
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def print_time_intervals(var_data: dict[str, dict[str, list[tuple[int, int]]]], variables: dict[str, str]) -> None:
    """Pretty-print time intervals for variables (debug helper, kept from the notebook)."""
    for var, days in var_data.items():
        print(f"{var}: {variables.get(var, var)}:")
        for day, intervals in days.items():
            print(f"  {day}: {intervals}")
        print()


@dataclass
class AssignmentContext:
    variables: dict[str, str]
    slots: dict[str, dict[str, list[tuple[int, int]]]]
    daily_domains: dict[str, list[int]]
    schedule: list[str | None]
    general_domain_reduced: list[int]
    points_to_remove: list[int]

    def remove_slot(self, slot: int) -> None:
        if slot in self.general_domain_reduced:
            self.general_domain_reduced.remove(slot)
        self.points_to_remove.append(slot)
