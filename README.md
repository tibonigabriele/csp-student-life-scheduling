# csp-student-life-scheduling

![CI](https://github.com/tibonigabriele/csp-student-life-scheduling/actions/workflows/ci.yml/badge.svg)

A small **CSP-inspired** weekly schedule builder for “student life” activities.

The original project started as a single Jupyter notebook; this repository turns it into a clean, reproducible
Python package with a **CLI** and a **JSON** export format.

## What it does

- Uses 5-minute slots over a whole week (7 × 288 = **2016** slots).
- Fills **fixed activities** from predefined time windows (classes, commute, sleep, meals, …).
- Assigns **flexible activities** using simple block-based heuristics:
  - study time (weekday target + weekend cap),
  - workout (3 days × 45min),
  - shopping (1 × 60min),
  - cleaning (1 × 60min),
  - personal time windows.
- Exports the final schedule as a per-day list of `{start, end, activity}` items (JSON).

## Quickstart

### Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -e ".[dev]"
```

### Run

```bash
csp-student-life --out schedule.json
# or: python -m csp_student_life.cli --out schedule.json
```

JSON shape:

```json
{
  "Monday": [
    {"start": "00:00", "end": "06:30", "activity": "Sleep"}
  ],
  "Tuesday": []
}
```

### Notebook

The original notebook is preserved in:

- `notebooks/CSP_for_Student_Life_Scheduling.ipynb`

## Development

```bash
pytest
ruff check .
```

## License

MIT. See `LICENSE`.
