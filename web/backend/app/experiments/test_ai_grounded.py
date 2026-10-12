
from typing import cast

from app.database import SessionLocal
from app.models import University, Program

from app.services.admission_retrieval import (
    get_verified_requirements,
    format_requirements_for_ai,
)
from app.ai.grounded import get_grounded_assessment


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
            raise ValueError("University not found.")

        program = (
            db.query(Program)
            .filter(
                Program.university_id == university.id,
                Program.name == "Computer Science",
            )
            .first()
        )

        if program is None:
            raise ValueError("Program not found.")

        requirements = get_verified_requirements(
            db=db,
            university_id=cast(int, university.id),
            program_id=cast(int, program.id),
            applicant_country="Nigeria",
            credential_type="WAEC",
        )

        if not requirements:
            raise ValueError(
                "No sourced admission requirements found."
            )

        verified_context = format_requirements_for_ai(
            requirements
        )

    finally:
        db.close()

    print("AI METHOD 2: SOURCE-GROUNDED AI")
    print("=" * 50)

    print("Student country: Nigeria")
    print("Credential: WAEC")
    print("Results: ['Mathematics: A1']")
    print(f"University: {university.name}")
    print(f"Program: {program.name}")

    print("\nRETRIEVED REQUIREMENTS")
    print("-" * 50)
    print(verified_context)

    print("\nGROUNDED AI RESPONSE")
    print("-" * 50)

    response = get_grounded_assessment(
        student_country="Nigeria",
        credential_type="WAEC",
        academic_results=["Mathematics: A1"],
        university=cast(str, university.name),
        program=cast(str, program.name),
        verified_requirements=verified_context,
    )

    print(response)


if __name__ == "__main__":
    main()
