from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session
from app.dependencies import get_db

from app.database import engine, Base
from app.models import (Student, AcademicCredential, AcademicResult,)
from app.schemas import (StudentCreate, StudentResponse, AcademicCredentialCreate, AcademicCredentialResponse,)
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "AI University Match For Students"}

@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        email=student.email,
        country=student.country,
        education_level=student.education_level,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.post(
    "/students/{student_index}/credentials",
    response_model=AcademicCredentialResponse,
)
def create_academic_credential(
    student_index: str,
    credential: AcademicCredentialCreate,
    db: Session = Depends(get_db),
):
    student = (
        db.query(Student)
        .filter(Student.student_index == student_index)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    new_credential = AcademicCredential(
        student_id=student.id,
        country=student.country,
        credential_type=credential.credential_type,
    )

    db.add(new_credential)
    db.flush()

    for result in credential.results:
        new_result = AcademicResult(
            credential_id=new_credential.id,
            subject=result.subject,
            grade=result.grade,
        )

        db.add(new_result)

    db.commit()
    db.refresh(new_credential)

    return new_credential