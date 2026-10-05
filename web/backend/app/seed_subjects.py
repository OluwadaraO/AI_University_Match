from app.database import SessionLocal
from app.models import AcademicSubject


NIGERIA_WAEC_SUBJECTS = [
    "English Language",
    "Mathematics",
    "Biology",
    "Chemistry",
    "Physics",
    "Economics",
    "Government",
    "Geography",
    "Commerce",
    "Financial Accounting",
    "Agricultural Science",
    "Further Mathematics",
    "Literature in English",
    "Civic Education",
    "Computer Studies",
    "Yoruba",
    "Igbo",
    "Hausa",
]

def seed_waec_subjects():
    db = SessionLocal()

    try:
        for subject_name in NIGERIA_WAEC_SUBJECTS:
            existing_subject = (
                db.query(AcademicSubject)
                .filter(
                    AcademicSubject.country == "Nigeria",
                    AcademicSubject.credential_type == "WAEC",
                    AcademicSubject.subject_name == subject_name,
                )
                .first()
            )

            if existing_subject is None:
                subject = AcademicSubject(
                    country="Nigeria",
                    credential_type="WAEC",
                    subject_name=subject_name,
                )

                db.add(subject)

        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed_waec_subjects()