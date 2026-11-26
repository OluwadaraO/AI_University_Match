from types import SimpleNamespace

from app.services.aggregate_matcher import (
    evaluate_aggregate_requirements,
)


def make_requirement(**kwargs):
    values = {
        "credential_type": "WAEC",
        "minimum_credit_count": None,
        "minimum_credit_grade": None,
        "minimum_gpa": None,
        "gpa_scale": None,
        "minimum_percentage": None,
    }

    values.update(kwargs)

    return SimpleNamespace(**values)


def make_results(grades):
    return {
        f"subject_{index}": SimpleNamespace(grade=grade)
        for index, grade in enumerate(grades)
    }


def run_tests():
    credit_requirement = make_requirement(
        minimum_credit_count=5,
        minimum_credit_grade="C6",
    )

    cases = [
        (
            "Exactly five credits",
            credit_requirement,
            ["A1", "B2", "B3", "C4", "C6"],
            "SATISFIED",
        ),
        (
            "More than five credits",
            credit_requirement,
            ["A1", "B2", "B3", "C4", "C5", "C6"],
            "SATISFIED",
        ),
        (
            "Insufficient recorded credits",
            credit_requirement,
            ["A1", "B2", "C6", "D7", "F9"],
            "UNKNOWN",
        ),
        (
            "No academic results",
            credit_requirement,
            [],
            "UNKNOWN",
        ),
        (
            "Exact minimum grade boundary",
            credit_requirement,
            ["C6", "C6", "C6", "C6", "C6"],
            "SATISFIED",
        ),
        (
            "Grades below minimum",
            credit_requirement,
            ["D7", "D7", "E8", "F9", "F9"],
            "UNKNOWN",
        ),
        (
            "Missing verified GPA",
            make_requirement(
                minimum_gpa=2.5,
                gpa_scale=4.0,
            ),
            ["A1", "A1", "A1", "A1", "A1"],
            "UNKNOWN",
        ),
        (
            "Missing percentage average",
            make_requirement(
                minimum_percentage=75.0,
            ),
            ["A1", "A1", "A1", "A1", "A1"],
            "UNKNOWN",
        ),
        (
            "Unspecified credential scale",
            make_requirement(
                credential_type=None,
                minimum_credit_count=5,
                minimum_credit_grade="C6",
            ),
            ["A1", "A1", "A1", "A1", "A1"],
            "UNKNOWN",
        ),
    ]

    for name, requirement, grades, expected in cases:
        results = evaluate_aggregate_requirements(
            requirement,
            make_results(grades),
        )

        actual = results[0]["status"]

        assert actual == expected, (
            f"{name}: expected {expected}, got {actual}"
        )

        print(f"PASS: {name}")

    print(f"\nAll {len(cases)} aggregate matching tests passed!")


if __name__ == "__main__":
    run_tests()