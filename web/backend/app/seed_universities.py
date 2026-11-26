import json
from pathlib import Path

from app.database import SessionLocal
from app.models import University, Program


DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "universities.json"
)


def seed_universities():
    db = SessionLocal()

    universities_added = 0
    programs_added = 0

    try:
        with DATA_PATH.open(encoding="utf-8") as file:
            universities = json.load(file)

        for entry in universities:

            university = (
                db.query(University)
                .filter(
                    University.name == entry["name"],
                    University.country == entry["country"],
                )
                .first()
            )

            if university is None:
                university = University(
                    name=entry["name"],
                    country=entry["country"],
                )

                db.add(university)
                db.flush()

                universities_added += 1

            for program_name in entry["programs"]:

                program = (
                    db.query(Program)
                    .filter(
                        Program.university_id == university.id,
                        Program.name == program_name,
                    )
                    .first()
                )

                if program is None:
                    program = Program(
                        university_id=university.id,
                        name=program_name,
                    )

                    db.add(program)
                    programs_added += 1

        db.commit()

        print("University data seeded successfully.")
        print(f"Universities added: {universities_added}")
        print(f"Programs added: {programs_added}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_universities()