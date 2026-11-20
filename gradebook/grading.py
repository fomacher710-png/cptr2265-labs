"""Pure grading rules: no files, no database, no network.

These functions are the easiest place to start writing unit tests. Each one
has normal cases, boundary values and error conditions worth testing.
"""

from numbers import Real

# (minimum percentage, letter) from highest to lowest
LETTER_SCALE = [
    (93, "A"), (90, "A-"),
    (87, "B+"), (83, "B"), (80, "B-"),
    (77, "C+"), (73, "C"), (70, "C-"),
    (67, "D+"), (60, "D"),
    (0, "F"),
]

GRADE_POINTS = {
    "A": 4.0, "A-": 3.67,
    "B+": 3.33, "B": 3.0, "B-": 2.67,
    "C+": 2.33, "C": 2.0, "C-": 1.67,
    "D+": 1.33, "D": 1.0,
    "F": 0.0,
}


def _check_score(score):
    # bool is a subclass of int in Python, but True is not a score.
    if isinstance(score, bool) or not isinstance(score, Real):
        raise TypeError(f"score must be a number, got {type(score).__name__}")
    if score < 0 or score > 100:
        raise ValueError(f"score must be between 0 and 100, got {score}")


def letter_grade(score):
    """Convert a percentage (0-100 inclusive) to a letter grade.

    Raises TypeError for non-numbers and ValueError for scores out of range.
    """
    _check_score(score)
    for minimum, letter in LETTER_SCALE:
        if score >= minimum:
            return letter
    return "F"  # unreachable, kept for safety


def grade_points(letter):
    """Return the 4.0-scale grade points for a letter grade (case-insensitive)."""
    if not isinstance(letter, str):
        raise TypeError("letter must be a string")
    key = letter.strip().upper()
    if key not in GRADE_POINTS:
        raise ValueError(f"unknown letter grade: {letter!r}")
    return GRADE_POINTS[key]


def drop_lowest(scores, n=1):
    """Return a new list with the n lowest scores removed.

    The original list is not modified. Order of the remaining scores is kept.
    Raises ValueError if n is negative or would remove every score.
    """
    if n < 0:
        raise ValueError("n must not be negative")
    if n >= len(scores):
        raise ValueError("cannot drop every score")
    for s in scores:
        _check_score(s)
    if n == 0:
        return list(scores)
    to_drop = sorted(scores)[:n]
    result = list(scores)
    for s in to_drop:
        result.remove(s)
    return result


def weighted_average(scores_by_category, weights):
    """Compute a weighted course percentage, rounded to 2 decimals.

    scores_by_category: e.g. {"labs": [90, 85], "exams": [78]}
    weights:            e.g. {"labs": 0.6, "exams": 0.4}

    Rules:
      * weights must be non-negative and add up to 1.0
      * every weighted category must have at least one score
      * categories in scores that have no weight are an error
    """
    if not weights:
        raise ValueError("weights must not be empty")
    if any(w < 0 for w in weights.values()):
        raise ValueError("weights must not be negative")
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("weights must add up to 1.0")

    extra = set(scores_by_category) - set(weights)
    if extra:
        raise ValueError(f"no weight given for: {sorted(extra)}")

    total = 0.0
    for category, weight in weights.items():
        scores = scores_by_category.get(category)
        if not scores:
            raise ValueError(f"no scores for category: {category}")
        for s in scores:
            _check_score(s)
        total += weight * (sum(scores) / len(scores))
    return round(total, 2)
