from __future__ import annotations

import argparse

from .schedule import build_schedule, schedule_to_jsonable, write_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="csp-student-life",
        description="Build a weekly student-life schedule (5-minute slots) and export it as JSON.",
    )
    parser.add_argument("--out", "-o", default="schedule.json", help="Output JSON path.")
    parser.add_argument(
        "--minify",
        action="store_true",
        help="Write minified JSON (no indentation).",
    )
    args = parser.parse_args(argv)

    flat = build_schedule()
    payload = schedule_to_jsonable(flat)
    write_json(payload, args.out, pretty=not args.minify)

    print(f"Wrote JSON schedule to: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
