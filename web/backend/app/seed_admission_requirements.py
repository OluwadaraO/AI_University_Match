import json
from datetime import date
from pathlib import Path

from app.database import SessionLocal
from app.models import (
    University,
    Program,
    AdmissionRequirement,
    AdmissionSubjectRequirement,
    AdmissionSource,
)


DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "admission_requirements.json"
)


def seed_admission_requirements():
    db = SessionLocal()

    created = 0
    updated = 0

    try:
        with DATA_PATH.open(encoding="utf-8") as file:
            entries = json.load(file)

        for entry in entries:

            university = (
                db.query(University)
                .filter(
                    University.name == entry["university"],
                    University.country == "United States",
                )
                .one_or_none()
            )

            if university is None:
                raise ValueError(
                    f"University not found: {entry['university']}"
                )

            program_id = None

            if entry.get("program") is not None:

                program = (
                    db.query(Program)
                    .filter(
                        Program.university_id == university.id,
                        Program.name == entry["program"],
                    )
                    .one_or_none()
                )

                if program is None:
                    raise ValueError(
                        f"Program not found: {entry['program']}"
                    )

                program_id = program.id

            requirement = (
                db.query(AdmissionRequirement)
                .filter(
                    AdmissionRequirement.university_id
                    == university.id,
                    AdmissionRequirement.program_id
                    == program_id,
                    AdmissionRequirement.applicant_country
                    == entry["applicant_country"],
                    AdmissionRequirement.credential_type
                    == entry.get("credential_type"),
                    AdmissionRequirement.requirement_type
                    == entry["requirement_type"],
                )
                .one_or_none()
            )

            if requirement is None:

                requirement = AdmissionRequirement(
                    university_id=university.id,
                    program_id=program_id,
                    applicant_country=entry["applicant_country"],
                    credential_type=entry.get("credential_type"),
                    requirement_type=entry["requirement_type"],
                )

                db.add(requirement)
                db.flush()

                created += 1

            else:
                updated += 1

            requirement.minimum_credit_count = entry.get(
                "minimum_credit_count"
            )

            requirement.minimum_credit_grade = entry.get(
                "minimum_credit_grade"
            )

            requirement.minimum_gpa = entry.get(
                "minimum_gpa"
            )

            requirement.gpa_scale = entry.get(
                "gpa_scale"
            )

            requirement.minimum_percentage = entry.get(
                "minimum_percentage"
            )

            # Replace the managed requirements and sources
            # with the current dataset contents.

            requirement.subject_requirements.clear()
            requirement.sources.clear()

            db.flush()

            for subject in entry.get("subject_requirements", []):

                requirement.subject_requirements.append(
                    AdmissionSubjectRequirement(
                        subject=subject["subject"],
                        requirement_level=subject["requirement_level"],
                        minimum_grade=subject.get("minimum_grade"),
                        minimum_years=subject.get("minimum_years"),
                        minimum_course_level=subject.get(
                            "minimum_course_level"
                        ),
                    )
                )

            for source in entry["sources"]:

                requirement.sources.append(
                    AdmissionSource(
                        source_title=source["source_title"],
                        source_url=source["source_url"],
                        verified_date=date.fromisoformat(
                            source["verified_date"]
                        ),
                        evidence_text=source.get("evidence_text"),
                        admission_cycle=source.get("admission_cycle"),
                    )
                )

            print(
                f"Processed: {university.name} | "
                f"{entry.get('program') or 'University-wide'}"
            )

        db.commit()

        print("\nAdmission requirements seeded successfully.")
        print(f"Requirements created: {created}")
        print(f"Requirements updated: {updated}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_admission_requirements()