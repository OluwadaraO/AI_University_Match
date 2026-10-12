from app.database import SessionLocal
from app.models import University, Program


def seed_universities():
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
            university = University(
                name="University of Illinois Urbana-Champaign",
                country="United States",
            )

            db.add(university)
            db.flush()

        program = (
            db.query(Program)
            .filter(
                Program.university_id == university.id,
                Program.name == "Computer Science",
            )
            .first()
        )

        if program is None:
            program = Program(
                university_id=university.id,
                name="Computer Science",
            )

            db.add(program)

        db.commit()

        print("University data seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_universities()