import json
from pathlib import Path

DATA_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "nigeria_academics.json"
)

def load_nigerian_academic_data():
    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    return data

def validate_nigerian_credential_config(
    credential_type: str,
    results
):
    data = load_nigerian_academic_data()
    credential_type = credential_type.upper()
    credentials = data["credentials"]
    if credential_type not in credentials:
        raise ValueError(
            f"{credential_type} is not a supported Nigerian credential."
        )
    credential_data = credentials[credential_type]
    valid_subjects = credential_data["subjects"]
    valid_grades = credential_data["grades"]
    for result in results:
        if result.subject not in valid_subjects:
            raise ValueError(
                f"{result.subject} is not a valid subject for {credential_type}."
            )
        grade = result.grade.upper()

        if grade not in valid_grades:
            raise ValueError(
                f"{grade} is not a valid grade for {credential_type}."
            )