"""Example tests to show the structure. Lab 9 asks for at least 15 test cases:
normal inputs, boundary values and error conditions. Add yours below.

Run from lab09/starter:
    pytest
    pytest --cov=gradebook --cov-report=term-missing --cov-report=html
"""

import pytest

from gradebook.grading import letter_grade, weighted_average
from gradebook.grading import grade_points, drop_lowest


def test_letter_grade_normal_score_returns_b():
    assert letter_grade(85) == "B"


def test_letter_grade_above_100_raises_value_error():
    with pytest.raises(ValueError):
        letter_grade(100.5)


# TODO: boundary values (exactly 93? 92.99? 0? 100?), drop_lowest, grade_points,
#       weighted_average, roster_loader, repository, service ...

@pytest.mark.parametrize("letter, expected_points", [
    ("A", 4.0),
    ("B", 3.0),
    ("C", 2.0),
    ("D", 1.0),
    ("F", 0.0),
])
def test_grade_points_normal(letter, expected_points):
    assert grade_points(letter) == expected_points


def test_grade_points_errors():
    with pytest.raises(ValueError):
        grade_points("Z")
    with pytest.raises(TypeError):
        grade_points(4.0)


# --- drop_lowest tests ---

def test_drop_lowest_normal():
    assert drop_lowest([80, 90, 70, 100], n=1) == [80, 90, 100]
    assert drop_lowest([50, 60, 70, 80], n=2) == [70, 80]
    assert drop_lowest([50, 60, 70], n=0) == [50, 60, 70]


def test_drop_lowest_errors():
    with pytest.raises(ValueError):
        drop_lowest([80, 90], n=-1)
    with pytest.raises(ValueError):
        drop_lowest([80, 90], n=2)
    with pytest.raises(ValueError):
        drop_lowest([80, 105], n=1)  # Invalid score inside list
    with pytest.raises(TypeError):
        drop_lowest(["80", 90], n=1)


# --- weighted_average tests ---

def test_weighted_average_normal():
    scores = {"labs": [90, 80], "exams": [100]}
    weights = {"labs": 0.5, "exams": 0.5}
    # labs avg = 85, exams avg = 100 -> (85 * 0.5) + (100 * 0.5) = 92.5
    assert weighted_average(scores, weights) == 92.5


def test_weighted_average_errors():
    scores = {"labs": [90]}
    
    # Empty weights
    with pytest.raises(ValueError):
        weighted_average(scores, {})
        
    # Negative weight
    with pytest.raises(ValueError):
        weighted_average(scores, {"labs": -0.5})
        
    # Weights don't sum to 1.0
    with pytest.raises(ValueError):
        weighted_average(scores, {"labs": 0.8})
        
    # Unweighted category present in scores
    with pytest.raises(ValueError):
        weighted_average({"labs": [90], "quizzes": [80]}, {"labs": 1.0})
        
    # Missing scores for a weighted category
    with pytest.raises(ValueError):
        weighted_average({"labs": []}, {"labs": 1.0})

def class_statistics(percentages):
    """Return mean, median, minimum, and maximum for a list of percentage scores.

    Raises ValueError if percentages is empty or contains invalid scores.
    """
    if not percentages:
        raise ValueError("percentages must not be empty")
    
    for s in percentages:
        _check_score(s)
        
    sorted_scores = sorted(percentages)
    n = len(sorted_scores)
    
    mean = sum(percentages) / n
    minimum = sorted_scores[0]
    maximum = sorted_scores[-1]
    
    if n % 2 == 1:
        median = float(sorted_scores[n // 2])
    else:
        mid1 = sorted_scores[(n // 2) - 1]
        mid2 = sorted_scores[n // 2]
        median = (mid1 + mid2) / 2.0
        
    return {
        "mean": round(mean, 2),
        "median": median,
        "minimum": minimum,
        "maximum": maximum
    }