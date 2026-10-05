from sqlalchemy.orm import Session
from app.models import AcademicSubject

VALID_CREDENTIAL_TYPES = {
    "WAEC",
}

VALID_GRADES = {
    "A1",
    "B2",
    "B3",
    "C4",
    "C5",
    "C6",
    "D7",
    "E8",
    "F9",
}

def validate_nigerian_credential(db: Session, credential_type: str, results):
    credential_type = credential_type.upper()

    if credential_type not in VALID_CREDENTIAL_TYPES:
        raise ValueError(
            f"{credential_type} is not a supported Nigerian credential."
        )

    for result in results:
        subject = (
                db.query(AcademicSubject)
                .filter(
                    AcademicSubject.country == "Nigeria",
                    AcademicSubject.credential_type == credential_type,
                    AcademicSubject.subject_name == result.subject,
                )
                .first()
            )

        if subject is None:
            raise ValueError(
                f"{result.subject} is not a valid subject for {credential_type}."
            )

        grade = result.grade.upper()

        if grade not in VALID_GRADES:
            raise ValueError(
                f"{grade} is not a valid grade for {credential_type}."
            )