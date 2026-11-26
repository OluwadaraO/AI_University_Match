from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session
from app.dependencies import get_db

from fastapi import status
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.security.dependencies import get_current_user

from app.models import (Student, AcademicCredential, AcademicResult,)
from app.schemas import (StudentCreate, StudentResponse,  StudentUpdate, AcademicCredentialCreate, AcademicCredentialResponse,)
from app.validators import validate_nigerian_credential
from app.routers import auth_router

from app.routers.recommendations import (
    router as recommendations_router,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(auth_router)
app.include_router(recommendations_router)

@app.get("/")
def root():
    return {"message": "AI University Match For Students"}

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check whether this user already has a student profile
    existing_student = (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have a student profile",
        )

    # Create a student profile linked to the logged-in user
    new_student = Student(
        user_id=current_user.id,
        email=current_user.email,
        country=student.country,
        education_level=student.education_level,
    )

    db.add(new_student)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create student profile. A profile may already exist.",
        )

    db.refresh(new_student)

    return new_student


@app.get(
    "/students/me",
    response_model=StudentResponse,
)
def get_my_student_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    return student

@app.patch(
    "/students/me",
    response_model=StudentResponse,
)
def update_my_student_profile(
    student_update: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    student.education_level = student_update.education_level

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(student)

    return student

@app.get(
    "/students/me/credentials",
    response_model=list[AcademicCredentialResponse],
)
def get_my_academic_credentials(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    credentials = (
        db.query(AcademicCredential)
        .filter(AcademicCredential.student_id == student.id)
        .order_by(AcademicCredential.id)
        .all()
    )

    return credentials


@app.post(
    "/students/{student_index}/credentials",
    response_model=AcademicCredentialResponse,
)
def create_academic_credential(
    student_index: str,
    credential: AcademicCredentialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = (
        db.query(Student)
        .filter(
            Student.student_index == student_index,
            Student.user_id == current_user.id,
        )
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    existing_credential = (
    db.query(AcademicCredential)
    .filter(
        AcademicCredential.student_id == student.id,
        AcademicCredential.credential_type == credential.credential_type,
    )
    .first()
)

    if existing_credential:
        raise HTTPException(
            status_code=409,
            detail="This credential already exists. Please update your existing results.",
        )

    if not credential.results:
        raise HTTPException(
            status_code=400,
            detail="At least one academic result is required",
        )

    subjects = [
        result.subject.strip().casefold()
        for result in credential.results
    ]

    if len(subjects) != len(set(subjects)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate subjects are not allowed",
            )
    if student.country.lower() == "nigeria":
        try:
            validate_nigerian_credential(
                db,
                credential.credential_type,
                credential.results,
            )
        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Academic credential validation is not supported for {student.country}",
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



@app.put(
    "/students/{student_index}/credentials/{credential_id}",
    response_model=AcademicCredentialResponse,
)
def update_academic_credential(
    student_index: str,
    credential_id: int,
    credential: AcademicCredentialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Verify that the student belongs to the logged-in user
    student = (
        db.query(Student)
        .filter(
            Student.student_index == student_index,
            Student.user_id == current_user.id,
        )
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    # 2. Find the credential belonging to this student
    existing_credential = (
        db.query(AcademicCredential)
        .filter(
            AcademicCredential.id == credential_id,
            AcademicCredential.student_id == student.id,
        )
        .first()
    )

    if existing_credential is None:
        raise HTTPException(
            status_code=404,
            detail="Academic credential not found",
        )

    # 3. Prevent changing the credential type through this endpoint
    if (
        credential.credential_type.lower()
        != existing_credential.credential_type.lower()
    ):
        raise HTTPException(
            status_code=400,
            detail="Credential type cannot be changed",
        )

    # 4. Validate the complete replacement results
    if student.country.lower() == "nigeria":
        try:
            validate_nigerian_credential(
                db,
                credential.credential_type,
                credential.results,
            )
        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Academic credential validation is not supported for {student.country}",
        )

    # 5. Reject duplicate subjects
    subjects = [
        result.subject.strip().casefold()
        for result in credential.results
    ]

    if len(subjects) != len(set(subjects)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate subjects are not allowed",
        )

    if not credential.results:
        raise HTTPException(
            status_code=400,
            detail="At least one academic result is required",
        )

    # 6. Replace the old results with the validated new results
    try:
        db.query(AcademicResult).filter(
            AcademicResult.credential_id == existing_credential.id
        ).delete(synchronize_session=False)

        for result in credential.results:
            db.add(
                AcademicResult(
                    credential_id=existing_credential.id,
                    subject=result.subject,
                    grade=result.grade,
                )
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    # 7. Reload the credential with its updated results
    db.expire_all()

    updated_credential = (
        db.query(AcademicCredential)
        .filter(
            AcademicCredential.id == credential_id,
        )
        .first()
    )

    return updated_credential

