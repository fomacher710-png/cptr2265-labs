"""Load a class roster with scores from a CSV file.

This module touches the FILE SYSTEM, so it is a natural dependency to replace
with a mock in Lab 10 (for example with unittest.mock.patch or by passing a
fake loader into GradebookService).

Expected CSV columns (header row required):
    student_id,name,category,score
"""

import csv

REQUIRED_COLUMNS = ("student_id", "name", "category", "score")


def load_roster(path):
    """Read the CSV at `path` and return a list of dicts:

        [{"student_id": "S001", "name": "Ana Lopez",
          "category": "labs", "score": 92.0}, ...]

    Raises FileNotFoundError if the file is missing and ValueError (mentioning
    the line number) for a missing column, blank field or non-numeric score.
    """
    records = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing column(s): {', '.join(missing)}")

        for line_no, row in enumerate(reader, start=2):
            for col in REQUIRED_COLUMNS:
                if not (row.get(col) or "").strip():
                    raise ValueError(f"line {line_no}: blank {col}")
            try:
                score = float(row["score"])
            except ValueError:
                raise ValueError(f"line {line_no}: score is not a number: {row['score']!r}")
            records.append({
                "student_id": row["student_id"].strip(),
                "name": row["name"].strip(),
                "category": row["category"].strip().lower(),
                "score": score,
            })
    return records
