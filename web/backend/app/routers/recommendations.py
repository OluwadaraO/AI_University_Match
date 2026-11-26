from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Student, User
from app.security.dependencies import get_current_user

from app.schemas.recommendation import RecommendationResponse

from app.services.recommendation_service import (
    generate_recommendations,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

@router.get(
    "/me",
    response_model=RecommendationResponse,
)
def get_my_recommendations(
    intended_major: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    use_ai: bool = Query(default=True),
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

    if student.country.strip().lower() != "nigeria":
        raise HTTPException(
            status_code=400,
            detail=(
                "This recommendation engine "
                "currently supports Nigeria."
            ),
        )

    return generate_recommendations(
        db=db,
        student=student,
        intended_major=intended_major,
        use_ai=use_ai,
    )