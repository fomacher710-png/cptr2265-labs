"""Demo: python -m gradebook [path/to/roster.csv]"""

import sqlite3
import sys

from .repository import StudentRepository
from .service import GradebookService

WEIGHTS = {"labs": 0.40, "quizzes": 0.20, "exams": 0.40}


def main(argv):
    path = argv[1] if len(argv) > 1 else "data/sample_roster.csv"
    service = GradebookService(StudentRepository(sqlite3.connect(":memory:")))
    count = service.import_roster(path)
    print(f"Imported {count} scores from {path}\n")
    print(f"{'ID':<6}{'Name':<18}{'Percent':>8}  Grade")
    for sid, name, percent, letter in service.class_report(WEIGHTS, drop_lowest_in="quizzes"):
        print(f"{sid:<6}{name:<18}{percent:>8.2f}  {letter}")


if __name__ == "__main__":
    main(sys.argv)
