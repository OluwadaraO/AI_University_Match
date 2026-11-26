from types import SimpleNamespace

from app.services.admission_matcher import (
    match_subject_requirement,
    meets_waec_minimum_grade,
)


def main():
    test_cases = [
        # Grade, minimum grade, years, course level, expected
        ("A1", "C6", None, None, "SATISFIED"),
        ("C6", "C6", None, None, "SATISFIED"),
        ("F9", "C6", None, None, "NOT_SATISFIED"),
        ("A1", None, 3.5, None, "UNKNOWN"),
        ("A1", None, None, "Trigonometry", "UNKNOWN"),
        ("A1", "C6", 3.5, None, "UNKNOWN"),
        ("F9", "C6", 3.5, None, "NOT_SATISFIED"),
        (None, "C6", None, None, "UNKNOWN"),
        ("INVALID", "C6", None, None, "UNKNOWN"),
        ("A1", None, None, None, "UNKNOWN"),
        ("A1", None, 3.5, "Trigonometry", "UNKNOWN"),
        ("A1", "INVALID", None, None, "UNKNOWN"),
    ]

    for index, case in enumerate(test_cases, start=1):
        grade, minimum_grade, years, level, expected = case

        student_result = (
            SimpleNamespace(
                subject="Mathematics",
                grade=grade,
            )
            if grade is not None
            else None
        )

        requirement = SimpleNamespace(
            subject="Mathematics",
            minimum_grade=minimum_grade,
            minimum_years=years,
            minimum_course_level=level,
        )

        result = match_subject_requirement(
            student_result,
            requirement,
        )

        assert result["status"] == expected, (
            f"Test {index} failed: "
            f"Expected {expected}, "
            f"got {result['status']}"
        )

        print(f"Test {index}: PASSED | {expected}")

    assert meets_waec_minimum_grade(" a1 ", "c6") is True
    assert meets_waec_minimum_grade(None, "C6") is None

    print(f"\nAll {len(test_cases) + 2} tests passed!")


if __name__ == "__main__":
    main()