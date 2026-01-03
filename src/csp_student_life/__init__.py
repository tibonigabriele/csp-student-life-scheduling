"""csp_student_life package.

Core idea: keep the original notebook as a demo, while moving all executable logic into
importable modules + a CLI.
"""

from .schedule import build_schedule, schedule_to_jsonable  # noqa: F401
