"""
Utilities for storing generated student test data.
"""

import json
from pathlib import Path


STUDENT_DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "generated"
    / "students.json"
)


def save_student_data(student: dict):
    """Save a student to the generated student data file."""

    STUDENT_DATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    students = []

    if STUDENT_DATA_FILE.exists():
        with open(
            STUDENT_DATA_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            students = json.load(file)

    students.append(student)

    with open(
        STUDENT_DATA_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            students,
            file,
            indent=4,
        )