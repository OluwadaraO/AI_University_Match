import time
from types import SimpleNamespace

from app.database import SessionLocal
from app.validators.nigeria import validate_nigerian_credential
from app.validators.nigeria_config import validate_nigerian_credential_config


TEST_CASES = [
    # --------------------
    # Valid results
    # --------------------
    {
        "name": "Valid Mathematics A1",
        "credential_type": "WAEC",
        "subject": "Mathematics",
        "grade": "A1",
        "expected": True,
    },
    {
        "name": "Valid English B2",
        "credential_type": "WAEC",
        "subject": "English Language",
        "grade": "B2",
        "expected": True,
    },
    {
        "name": "Valid Physics B3",
        "credential_type": "WAEC",
        "subject": "Physics",
        "grade": "B3",
        "expected": True,
    },
    {
        "name": "Valid Chemistry C4",
        "credential_type": "WAEC",
        "subject": "Chemistry",
        "grade": "C4",
        "expected": True,
    },
    {
        "name": "Valid Biology C5",
        "credential_type": "WAEC",
        "subject": "Biology",
        "grade": "C5",
        "expected": True,
    },
    {
        "name": "Valid Economics C6",
        "credential_type": "WAEC",
        "subject": "Economics",
        "grade": "C6",
        "expected": True,
    },
    {
        "name": "Valid Government D7",
        "credential_type": "WAEC",
        "subject": "Government",
        "grade": "D7",
        "expected": True,
    },
    {
        "name": "Valid Geography E8",
        "credential_type": "WAEC",
        "subject": "Geography",
        "grade": "E8",
        "expected": True,
    },
    {
        "name": "Valid Commerce F9",
        "credential_type": "WAEC",
        "subject": "Commerce",
        "grade": "F9",
        "expected": True,
    },

    # --------------------
    # Invalid subjects
    # --------------------
    {
        "name": "Invalid Basket Weaving subject",
        "credential_type": "WAEC",
        "subject": "Basket Weaving",
        "grade": "A1",
        "expected": False,
    },
    {
        "name": "Invalid Astronomy subject",
        "credential_type": "WAEC",
        "subject": "Astronomy",
        "grade": "B2",
        "expected": False,
    },
    {
        "name": "Invalid Robotics subject",
        "credential_type": "WAEC",
        "subject": "Robotics",
        "grade": "C4",
        "expected": False,
    },

    # --------------------
    # Invalid grades
    # --------------------
    {
        "name": "Invalid grade A2",
        "credential_type": "WAEC",
        "subject": "Mathematics",
        "grade": "A2",
        "expected": False,
    },
    {
        "name": "Invalid grade Z9",
        "credential_type": "WAEC",
        "subject": "Physics",
        "grade": "Z9",
        "expected": False,
    },
    {
        "name": "Invalid numeric grade",
        "credential_type": "WAEC",
        "subject": "Chemistry",
        "grade": "100",
        "expected": False,
    },

    # --------------------
    # Invalid credentials
    # --------------------
    {
        "name": "Invalid SAT credential",
        "credential_type": "SAT",
        "subject": "Mathematics",
        "grade": "A1",
        "expected": False,
    },
    {
        "name": "Invalid GCSE credential",
        "credential_type": "GCSE",
        "subject": "Mathematics",
        "grade": "A1",
        "expected": False,
    },
]

def create_result(subject, grade):
    return SimpleNamespace(
        subject=subject,
        grade=grade,
    )

def run_config_validator(test_case):
    result = create_result(
        test_case["subject"],
        test_case["grade"],
    )

    try:
        validate_nigerian_credential_config(
            test_case["credential_type"],
            [result],
        )
        return True

    except ValueError:
        return False

def run_database_validator(db, test_case):
    result = create_result(
        test_case["subject"],
        test_case["grade"],
    )

    try:
        validate_nigerian_credential(
            db,
            test_case["credential_type"],
            [result],
        )
        return True

    except ValueError:
        return False

def compare_methods():
    db = SessionLocal()

    database_correct = 0
    config_correct = 0

    database_start = time.perf_counter()

    try:
        for test_case in TEST_CASES:
            database_result = run_database_validator(
                db,
                test_case,
            )

            if database_result == test_case["expected"]:
                database_correct += 1

        database_end = time.perf_counter()

        config_start = time.perf_counter()

        for test_case in TEST_CASES:
            config_result = run_config_validator(
                test_case,
            )

            if config_result == test_case["expected"]:
                config_correct += 1

        config_end = time.perf_counter()

    finally:
        db.close()

    database_time = database_end - database_start
    config_time = config_end - config_start

    print("\n--- DATA LAYER COMPARISON ---")

    print(
        f"PostgreSQL Accuracy: "
        f"{database_correct}/{len(TEST_CASES)}"
    )

    print(
        f"JSON Accuracy: "
        f"{config_correct}/{len(TEST_CASES)}"
    )

    print(
        f"PostgreSQL Execution Time: "
        f"{database_time:.6f} seconds"
    )

    print(
        f"JSON Execution Time: "
        f"{config_time:.6f} seconds"
    )


if __name__ == "__main__":
    compare_methods()