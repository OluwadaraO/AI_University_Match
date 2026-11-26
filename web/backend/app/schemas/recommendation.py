from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


AssessmentStatus = Literal[
    "SATISFIED",
    "NOT_SATISFIED",
    "UNKNOWN",
]


class AdmissionSourceResponse(BaseModel):
    id: int
    title: str
    url: str
    verified_date: date
    evidence_text: str | None = None
    admission_cycle: str | None = None

class SubjectAssessmentResponse(BaseModel):
    requirement_id: int
    subject_requirement_id: int
    subject: str
    requirement_level: str
    student_grade: str | None = None
    minimum_grade: str | None = None
    minimum_years: float | None = None
    minimum_course_level: str | None = None
    status: AssessmentStatus
    reason: str
    sources: list[AdmissionSourceResponse]

class AggregateAssessmentResponse(BaseModel):
    requirement_id: int
    requirement_type: str
    requirement_level: str = "required"

    required_value: float | None = None
    student_value: float | None = None

    minimum_grade: str | None = None
    gpa_scale: float | None = None

    status: AssessmentStatus
    reason: str

    sources: list[AdmissionSourceResponse]

class ProgramRecommendationResponse(BaseModel):
    university_id: int
    university_name: str
    university_country: str
    program_id: int
    program_name: str

    academic_status: AssessmentStatus
    evaluated_requirements_status: AssessmentStatus

    explanation: str
    subject_assessments: list[SubjectAssessmentResponse]
    aggregate_assessments: list[AggregateAssessmentResponse] = Field(
        default_factory=list
    )
    requirements_complete: bool = False
    ai_generated: bool = False
    ai_verified: bool = False
    ai_assessment: str | None = None
    ai_revisions: int = 0

    disclaimer: str = (
        "This assessment is based on available academic "
        "evidence and does not guarantee admission."
    )


class RecommendationResponse(BaseModel):
    student_index: str
    student_country: str
    credential_type: str
    total_recommendations: int
    recommendations: list[ProgramRecommendationResponse]