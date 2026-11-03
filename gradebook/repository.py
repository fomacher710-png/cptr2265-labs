"""Store students and scores in a SQLite database.

This is a DATABASE dependency. For Lab 10 integration tests, create the
repository with an in-memory database so every test starts clean:

    repo = StudentRepository(sqlite3.connect(":memory:"))
"""

import sqlite3


class StudentRepository:
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._create_schema()

    def _create_schema(self):
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name       TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scores (
                student_id TEXT NOT NULL REFERENCES students(student_id),
                category   TEXT NOT NULL,
                score      REAL NOT NULL
            );
            """
        )
        self._conn.commit()

    def add_student(self, student_id, name):
        """Add a student, or update the name if the id already exists."""
        self._conn.execute(
            "INSERT INTO students (student_id, name) VALUES (?, ?) "
            "ON CONFLICT(student_id) DO UPDATE SET name = excluded.name",
            (student_id, name),
        )
        self._conn.commit()

    def add_score(self, student_id, category, score):
        if self.get_student_name(student_id) is None:
            raise KeyError(f"unknown student: {student_id}")
        self._conn.execute(
            "INSERT INTO scores (student_id, category, score) VALUES (?, ?, ?)",
            (student_id, category, score),
        )
        self._conn.commit()

    def get_student_name(self, student_id):
        row = self._conn.execute(
            "SELECT name FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()
        return row[0] if row else None

    def list_student_ids(self):
        rows = self._conn.execute(
            "SELECT student_id FROM students ORDER BY student_id"
        ).fetchall()
        return [r[0] for r in rows]

    def get_scores(self, student_id):
        """Return {"category": [score, ...], ...} for one student."""
        rows = self._conn.execute(
            "SELECT category, score FROM scores WHERE student_id = ? ORDER BY rowid",
            (student_id,),
        ).fetchall()
        result = {}
        for category, score in rows:
            result.setdefault(category, []).append(score)
        return result
