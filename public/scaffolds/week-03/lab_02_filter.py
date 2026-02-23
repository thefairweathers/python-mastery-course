"""
Lab 3.2: Data Filter Pipeline
==============================

Process and analyze a dataset using comprehensions and control flow.
You'll build a pipeline that filters, transforms, and summarizes
student grade data.
"""


STUDENTS = [
    {"name": "Alice", "grade": 92, "subject": "Math", "status": "active"},
    {"name": "Bob", "grade": 78, "subject": "Science", "status": "active"},
    {"name": "Charlie", "grade": 45, "subject": "Math", "status": "withdrawn"},
    {"name": "Diana", "grade": 88, "subject": "English", "status": "active"},
    {"name": "Eve", "grade": 95, "subject": "Math", "status": "active"},
    {"name": "Frank", "grade": 62, "subject": "Science", "status": "active"},
    {"name": "Grace", "grade": 71, "subject": "English", "status": "active"},
    {"name": "Hank", "grade": 84, "subject": "Math", "status": "active"},
    {"name": "Ivy", "grade": 39, "subject": "Science", "status": "withdrawn"},
    {"name": "Jack", "grade": 55, "subject": "English", "status": "active"},
]


def active_students(students: list[dict]) -> list[dict]:
    """
    Return only students whose status is "active".
    Use a list comprehension.
    """
    # TODO: Implement
    pass


def passing_students(students: list[dict], threshold: int = 50) -> list[dict]:
    """
    Return only students with a grade >= threshold.
    Use a list comprehension.
    """
    # TODO: Implement
    pass


def classify_grades(students: list[dict]) -> list[dict]:
    """
    Add a 'letter' key to each student dict based on their grade:
      90-100 → 'A', 80-89 → 'B', 70-79 → 'C', 60-69 → 'D', below 60 → 'F'

    Return a NEW list of dicts (don't modify the originals).

    Hint: Use match/case on the grade divided by 10, or if/elif chains.
    """
    # TODO: Implement
    pass


def subject_averages(students: list[dict]) -> dict[str, float]:
    """
    Calculate the average grade per subject for active, passing students.

    Return a dict like {"Math": 88.0, "Science": 70.0, "English": 79.5}
    Round averages to 1 decimal place.

    Hint: First filter, then group by subject using a dict comprehension
    or a loop with defaultdict.
    """
    # TODO: Implement
    pass


def honor_roll(students: list[dict]) -> list[str]:
    """
    Return a sorted list of names of active students with grade >= 85.
    Use a single list comprehension with multiple conditions, then sort.
    """
    # TODO: Implement
    pass


def summary_report(students: list[dict]) -> dict:
    """
    Generate a complete summary report. Return a dict with:
    - 'total': total number of students
    - 'active': number of active students
    - 'passing': number of active students with grade >= 50
    - 'failing': number of active students with grade < 50
    - 'highest': name of the active student with the highest grade
    - 'lowest': name of the active student with the lowest grade
    - 'honor_roll': sorted list of names with grade >= 85 (active only)
    """
    # TODO: Implement
    pass


# ============================================================
# Tests
# ============================================================

def test_active():
    result = active_students(STUDENTS)
    assert len(result) == 8, f"Expected 8 active, got {len(result)}"
    assert all(s["status"] == "active" for s in result)
    print("✓ active_students passed")


def test_passing():
    result = passing_students(STUDENTS)
    assert all(s["grade"] >= 50 for s in result)
    print("✓ passing_students passed")


def test_classify():
    result = classify_grades(STUDENTS)
    alice = next(s for s in result if s["name"] == "Alice")
    assert alice["letter"] == "A", f"Expected 'A', got '{alice['letter']}'"
    frank = next(s for s in result if s["name"] == "Frank")
    assert frank["letter"] == "D", f"Expected 'D', got '{frank['letter']}'"
    print("✓ classify_grades passed")


def test_averages():
    result = subject_averages(STUDENTS)
    assert "Math" in result
    assert "Science" in result
    print(f"  Subject averages: {result}")
    print("✓ subject_averages passed")


def test_honor_roll():
    result = honor_roll(STUDENTS)
    assert "Alice" in result
    assert "Eve" in result
    assert result == sorted(result), "Honor roll should be sorted"
    print("✓ honor_roll passed")


def test_summary():
    result = summary_report(STUDENTS)
    assert result["total"] == 10
    assert result["active"] == 8
    print(f"  Summary: {result}")
    print("✓ summary_report passed")


if __name__ == "__main__":
    test_active()
    test_passing()
    test_classify()
    test_averages()
    test_honor_roll()
    test_summary()
    print("\nAll tests passed! ✓")
