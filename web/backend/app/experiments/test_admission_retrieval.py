
from app.database import SessionLocal
from app.models import University, Program
from typing import cast
from app.services.admission_retrieval import (
    get_verified_requirements,
    format_requirements_for_ai,
)


def main():
    db = SessionLocal()

    try:
        university = (
            db.query(University)
            .filter(
                University.name ==
                "University of Illinois Urbana-Champaign"
            )
            .first()
        )

        if university is None:
            raise ValueError("UIUC was not found in the database.")

        program = (
            db.query(Program)
            .filter(
                Program.university_id == university.id,
                Program.name == "Computer Science",
            )
            .first()
        )

        if program is None:
            raise ValueError("Computer Science program not found.")

        requirements = get_verified_requirements(
            db=db,
            university_id=cast(int, university.id),
            program_id=cast(int, program.id),
            applicant_country="Nigeria",
            credential_type="WAEC",
        )

        print("SOURCE-GROUNDED RETRIEVAL TEST")
        print("=" * 50)

        print(f"University: {university.name}")
        print(f"Program: {program.name}")
        print(f"Requirements found: {len(requirements)}")
        print()

        formatted = format_requirements_for_ai(requirements)
        print(formatted)

        if not requirements:
            raise ValueError(
                "No sourced requirements were found. "
                "Check the seeded records and filters."
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()
