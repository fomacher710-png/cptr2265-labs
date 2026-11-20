"""Example tests to show the structure. Lab 9 asks for at least 15 test cases:
normal inputs, boundary values and error conditions. Add yours below.

Run from lab09/starter:
    pytest
    pytest --cov=gradebook --cov-report=term-missing --cov-report=html
"""

import pytest

from gradebook.grading import letter_grade

from gradebook.grading import class_statistics


def test_letter_grade_normal_score_returns_b():
    assert letter_grade(85) == "B"


def test_letter_grade_above_100_raises_value_error():
    with pytest.raises(ValueError):
        letter_grade(100.5)


from gradebook.grading import class_statistics


def test_class_statistics_normal():
    stats = class_statistics([80.0, 90.0, 100.0])
    assert stats["min"] == 80.0
    assert stats["max"] == 100.0
    assert stats["mean"] == 90.0
    assert stats["median"] == 90.0


def test_class_statistics_even_count():
    stats = class_statistics([70.0, 80.0, 90.0, 100.0])
    assert stats["min"] == 70.0
    assert stats["max"] == 100.0
    assert stats["mean"] == 85.0
    assert stats["median"] == 85.0


def test_class_statistics_empty_raises_value_error():
    with pytest.raises(ValueError):
        class_statistics([])


# TODO: boundary values (exactly 93? 92.99? 0? 100?), drop_lowest, grade_points,
#       weighted_average, roster_loader, repository, service ...
