from app.database import SessionLocal
from app.models import (
    Student,
    AcademicCredential,
    AcademicResult,
    University,
    Program,
    AdmissionRequirement,
    AdmissionSubjectRequirement,
)

from app.services.admission_matcher import match_subject_requirement


STUDENT_INDEX = "STU-2F7A41EB"


def test_admission_matcher():
    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.student_index == STUDENT_INDEX)
            .first()
        )

        if student is None:
            print("Student not found.")
            return

        math_result = (
            db.query(AcademicResult)
            .join(AcademicCredential)
            .filter(
                AcademicCredential.student_id == student.id,
                AcademicCredential.credential_type == "WAEC",
                AcademicResult.subject == "Mathematics",
            )
            .first()
        )

        if math_result is None:
            print("Student does not have a WAEC Mathematics result.")
            return

        university = (
            db.query(University)
            .filter(
                University.name
                == "University of Illinois Urbana-Champaign"
            )
            .first()
        )

        if university is None:
            print("UIUC not found.")
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
            print("Computer Science program not found.")
            return

        requirement = (
            db.query(AdmissionSubjectRequirement)
            .join(AdmissionRequirement)
            .filter(
                AdmissionRequirement.university_id == university.id,
                AdmissionRequirement.program_id == program.id,
                AdmissionSubjectRequirement.subject == "Mathematics",
            )
            .first()
        )

        if requirement is None:
            print("Mathematics requirement not found.")
            return

        result = match_subject_requirement(
            math_result,
            requirement,
        )

        print("Student:", student.student_index)
        print(
            "Student result:",
            math_result.subject,
            math_result.grade,
        )
        print("University:", university.name)
        print("Program:", program.name)
        print("Requirement:", requirement.subject)
        print("Minimum years:", requirement.minimum_years)
        print(
            "Minimum course level:",
            requirement.minimum_course_level,
        )
        print()
        print("MATCH RESULT")
        print("Status:", result["status"])
        print("Reason:", result["reason"])

    finally:
        db.close()


if __name__ == "__main__":
    test_admission_matcher()