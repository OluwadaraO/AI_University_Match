from app.services.admission_matcher import meets_waec_minimum_grade


test_cases = [
    ("A1", "C6", True),
    ("B3", "C6", True),
    ("C6", "C6", True),
    ("D7", "C6", False),
    ("F9", "C6", False),
    ("A1", "A1", True),
    ("B2", "A1", False),
]


for student_grade, minimum_grade, expected in test_cases:
    result = meets_waec_minimum_grade(
        student_grade,
        minimum_grade,
    )

    print(
        f"Student: {student_grade} | "
        f"Minimum: {minimum_grade} | "
        f"Result: {result} | "
        f"Expected: {expected}"
    )