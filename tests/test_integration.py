import pytest
from gradebook.grading import weighted_average, class_statistics

# --- Component 1: In-Memory Database / Repository ---
class InMemoryGradebookDB:
    """A real in-memory data store representing a database backend."""
    def __init__(self):
        self.students = {}

    def add_student(self, student_id: int, name: str, scores: dict):
        self.students[student_id] = {"name": name, "scores": scores}

    def get_student(self, student_id: int) -> dict:
        if student_id not in self.students:
            raise KeyError(f"Student ID {student_id} not found in database")
        return self.students[student_id]

    def get_all_students(self) -> list:
        return list(self.students.values())

    def clear(self):
        self.students.clear()


# --- Component 2: Service Layer ---
class GradebookService:
    """Coordinates business logic between the database and grading functions."""
    def __init__(self, db: InMemoryGradebookDB):
        self.db = db

    def calculate_student_final_grade(self, student_id: int, weights: dict) -> float:
        record = self.db.get_student(student_id)
        return weighted_average(record["scores"], weights)

    def generate_class_summary(self, weights: dict) -> dict:
        all_students = self.db.get_all_students()
        if not all_students:
            raise ValueError("No students found in the database")
        
        final_grades = [
            weighted_average(s["scores"], weights) for s in all_students
        ]
        return class_statistics(final_grades)


# --- Pytest Fixtures for Setup & Teardown ---
@pytest.fixture
def gradebook_db():
    """Setup: Initialize the in-memory database and populate sample data."""
    db = InMemoryGradebookDB()
    db.add_student(101, "Alice", {"labs": [90, 85], "exams": [95]})
    db.add_student(102, "Bob", {"labs": [70, 75], "exams": [80]})
    db.add_student(103, "Charlie", {"labs": [85, 90], "exams": [90]})
    
    yield db  # Provides the db to the test function
    
    # Teardown: Clear state after test runs
    db.clear()


@pytest.fixture
def gradebook_service(gradebook_db):
    """Setup: Wire the service layer to the populated database fixture."""
    return GradebookService(gradebook_db)


# --- Integration Tests ---

def test_integration_service_calculates_student_weighted_average(gradebook_service):
    """Integration Test 1: Service queries the in-memory DB and uses weighted_average 
    to compute a student's final score correctly.
    """
    weights = {"labs": 0.4, "exams": 0.6}
    
    # Alice: labs avg = 87.5, exams avg = 95 -> (87.5 * 0.4) + (95 * 0.6) = 35 + 57 = 92.0
    final_grade = gradebook_service.calculate_student_final_grade(101, weights)
    
    assert final_grade == 92.0


def test_integration_class_summary_statistics(gradebook_service):
    """Integration Test 2: Service pulls all records from the database, calculates 
    weighted averages across multiple students, and passes them into class_statistics.
    """
    weights = {"labs": 0.5, "exams": 0.5}
    
    # Alice final: (87.5 * 0.5) + (95 * 0.5) = 91.25
    # Bob final: (72.5 * 0.5) + (80 * 0.5) = 76.25
    # Charlie final: (87.5 * 0.5) + (90 * 0.5) = 88.75
    
    summary = gradebook_service.generate_class_summary(weights)
    
    assert summary["minimum"] == 76.25
    assert summary["maximum"] == 91.25
    assert summary["mean"] == 85.42


def test_integration_database_error_propagation(gradebook_service):
    """Integration Test 3: Verifies that database lookup errors propagate 
    properly through the service layer when querying invalid entities.
    """
    weights = {"labs": 0.5, "exams": 0.5}
    
    with pytest.raises(KeyError, match="Student ID 999 not found"):
        gradebook_service.calculate_student_final_grade(999, weights)