from datetime import date

from app.database import SessionLocal
from app.models import (
    University,
    Program,
    AdmissionRequirement,
    AdmissionSubjectRequirement,
    AdmissionSource,
)


def seed_admission_requirements():
    db = SessionLocal()

    try:
        university = (
            db.query(University)
            .filter(
                University.name
                == "University of Illinois Urbana-Champaign"
            )
            .first()
        )

        if university is None:
            print("UIUC was not found.")
            return

        program = (
            db.query(Program)
            .filter(
                Program.university_id == university.id,
                Program.name == "Computer Science",
            )
            .first()
        )

        if program is None:
            print("Computer Science program was not found.")
            return

        admission_requirement = AdmissionRequirement(
            university_id=university.id,
            program_id=program.id,
            applicant_country="Nigeria",
            credential_type=None,
            requirement_type="coursework",
        )

        db.add(admission_requirement)
        db.flush()

        math_requirement = AdmissionSubjectRequirement(
            admission_requirement_id=admission_requirement.id,
            subject="Mathematics",
            requirement_level="required",
            minimum_grade=None,
            minimum_years=3.5,
            minimum_course_level="Trigonometry or higher",
        )

        db.add(math_requirement)

        source = AdmissionSource(
            admission_requirement_id=admission_requirement.id,
            source_url="https://www.admissions.illinois.edu/first-year-requirements/",
            source_title="UIUC First-Year Requirements",
            verified_date=date.today(),
        )

        db.add(source)

        db.commit()

        print("UIUC Computer Science admission requirement seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_admission_requirements()