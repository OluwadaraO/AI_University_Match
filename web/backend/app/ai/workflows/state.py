from typing import TypedDict


class RecommendationState(TypedDict):
    student_country: str
    credential_type: str
    academic_results: list[str]

    university: str
    program: str

    verified_requirements: str
    expected_status: str

    initial_assessment: str
    assessment: str

    verified: bool
    issues: list[str]
    revisions: int

    error: str | None