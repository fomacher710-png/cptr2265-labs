"""Application service that ties the loader, repository and grading rules together.

Its dependencies are passed in through the constructor (dependency injection),
which makes it straightforward to substitute mocks or fakes in tests.
"""

from . import grading
from .roster_loader import load_roster


class GradebookService:
    def __init__(self, repository, loader=load_roster):
        self._repo = repository
        self._load = loader

    def import_roster(self, path):
        """Load a roster CSV into the repository. Returns the number of scores imported."""
        records = self._load(path)
        for r in records:
            self._repo.add_student(r["student_id"], r["name"])
            self._repo.add_score(r["student_id"], r["category"], r["score"])
        return len(records)

    def final_grade(self, student_id, weights, drop_lowest_in=None):
        """Return (percentage, letter) for one student.

        drop_lowest_in: optional category name whose single lowest score is
        dropped before averaging (only if that category has 2+ scores).
        """
        if self._repo.get_student_name(student_id) is None:
            raise KeyError(f"unknown student: {student_id}")
        scores = self._repo.get_scores(student_id)
        if drop_lowest_in and len(scores.get(drop_lowest_in, [])) > 1:
            scores[drop_lowest_in] = grading.drop_lowest(scores[drop_lowest_in], 1)
        percent = grading.weighted_average(scores, weights)
        return percent, grading.letter_grade(percent)

    def class_report(self, weights, drop_lowest_in=None):
        """Return a list of (student_id, name, percentage, letter), sorted by id."""
        report = []
        for sid in self._repo.list_student_ids():
            percent, letter = self.final_grade(sid, weights, drop_lowest_in)
            report.append((sid, self._repo.get_student_name(sid), percent, letter))
        return report
