
from app.ai.verification import verify_assessment


def main():
    test_cases = [
        (
            "Evaluation Status: UNKNOWN",
            "UNKNOWN",
            True,
        ),
        (
            "Evaluation Status: SATISFIED",
            "UNKNOWN",
            False,
        ),
        (
            "Evaluation Status: NOT_SATISFIED",
            "UNKNOWN",
            False,
        ),
        (
            "No clear status provided.",
            "UNKNOWN",
            False,
        ),
    ]

    for assessment, expected_status, expected_valid in test_cases:
        result = verify_assessment(
            assessment=assessment,
            expected_status=expected_status,
        )

        print(f"Assessment: {assessment}")
        print(f"Valid: {result.is_valid}")
        print(f"Issues: {result.issues}")
        print()

        assert result.is_valid == expected_valid

    print("All verification tests passed!")


if __name__ == "__main__":
    main()
