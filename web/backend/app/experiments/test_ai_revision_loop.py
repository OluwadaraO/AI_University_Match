
from typing import cast

from app.database import SessionLocal
from app.models import University, Program

from app.services.admission_retrieval import (
    get_verified_requirements,
    format_requirements_for_ai,
)
from app.ai.revision_loop import generate_verify_revise


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
            raise ValueError("No sourced requirements found.")

        verified_context = format_requirements_for_ai(
            requirements
        )

        university_name = str(university.name)
        program_name = str(program.name)

    finally:
        db.close()

    print("AI METHOD 3: GENERATE-VERIFY-REVISE")
    print("=" * 50)

    result = generate_verify_revise(
        student_country="Nigeria",
        credential_type="WAEC",
        academic_results=["Mathematics: A1"],
        university=university_name,
        program=program_name,
        verified_requirements=verified_context,
        expected_status="UNKNOWN",
    )

    print("\nINITIAL RESPONSE")
    print("-" * 50)
    print(result.initial_response)

    print("\nFINAL RESPONSE")
    print("-" * 50)
    print(result.final_response)

    print("\nVERIFICATION RESULTS")
    print("-" * 50)
    print(f"Status consistency passed: {result.verified}")
    print(f"Revisions performed: {result.revisions}")
    print(f"Remaining issues: {result.issues}")


if __name__ == "__main__":
    main()
