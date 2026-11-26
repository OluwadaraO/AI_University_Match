from sqlalchemy.orm import Session, selectinload

from app.models import (
    Student,
    AcademicCredential,
    University,
    Program,
)

from app.services.admission_matcher import (
    match_subject_requirement,
)

from app.services.admission_retrieval import (
    get_verified_requirements,
)

from app.schemas.recommendation import (
    AdmissionSourceResponse,
    SubjectAssessmentResponse,
    ProgramRecommendationResponse,
    RecommendationResponse,
    AggregateAssessmentResponse,
)

from app.services.ai_recommendation_service import (
    enhance_recommendation,
)

from app.services.aggregate_matcher import (
    evaluate_aggregate_requirements,
)

def get_student_waec_results(
    db: Session,
    student: Student,
):
    credentials = (
        db.query(AcademicCredential)
        .options(
            selectinload(AcademicCredential.results)
        )
        .filter(
            AcademicCredential.student_id == student.id,
            AcademicCredential.credential_type == "WAEC",
        )
        .all()
    )

    results_by_subject = {}

    for credential in credentials:
        for result in credential.results:
            subject = result.subject.strip().casefold()

            results_by_subject.setdefault(
                subject, []
            ).append(result)

    # Do not silently choose between conflicting grades.
    return {
        subject: results[0]
        for subject, results in results_by_subject.items()
        if len({
            result.grade.strip().upper()
            for result in results
        }) == 1
    }


def calculate_program_status(
    assessments: list[
        SubjectAssessmentResponse | AggregateAssessmentResponse
    ],
):
    required_assessments = [
        assessment
        for assessment in assessments
        if assessment.requirement_level.lower() == "required"
    ]

    if not required_assessments:
        return "UNKNOWN"

    statuses = [
        assessment.status
        for assessment in required_assessments
    ]

    if "NOT_SATISFIED" in statuses:
        return "NOT_SATISFIED"

    if "UNKNOWN" in statuses:
        return "UNKNOWN"

    return "SATISFIED"


def build_explanation(
    status: str,
    assessments: list[
        SubjectAssessmentResponse | AggregateAssessmentResponse
    ],
):
    if not assessments:
        return (
            "There are no sourced academic requirements "
            "available to evaluate this program."
        )

    if status == "NOT_SATISFIED":
        summary = (
            "The student does not meet at least one "
            "of the recorded mandatory academic requirements."
        )

    elif status == "UNKNOWN":
        summary = (
            "There is insufficient academic information "
            "to determine whether the student meets "
            "the recorded requirements."
        )

    else:
        summary = (
            "The student meets the evaluated mandatory "
            "academic requirements. However, complete "
            "admission eligibility has not been established."
        )

    details = []

    for assessment in assessments:
        if isinstance(assessment, SubjectAssessmentResponse):
            label = assessment.subject
        else:
            label = (
                assessment.requirement_type
                .replace("_", " ")
                .capitalize()
            )

        details.append(f"{label}: {assessment.reason}")

    return " ".join([summary, *details])


def evaluate_program(
    db: Session,
    student: Student,
    university: University,
    program: Program,
    student_results: dict,
):
    requirements = get_verified_requirements(
        db=db,
        university_id=university.id,
        program_id=program.id,
        applicant_country=student.country,
        credential_type="WAEC",
    )

    assessments = []
    aggregate_assessments = []

    for requirement in requirements:

        sources = [
            AdmissionSourceResponse(
                id=source.id,
                title=source.source_title,
                url=source.source_url,
                verified_date=source.verified_date,
                evidence_text=source.evidence_text,
                admission_cycle=source.admission_cycle,
            )
            for source in requirement.sources
        ]

        aggregate_results = evaluate_aggregate_requirements(
            requirement=requirement,
            student_results=student_results,
        )

        for result in aggregate_results:
            aggregate_assessments.append(
                AggregateAssessmentResponse(
                    requirement_id=requirement.id,
                    sources=sources,
                    **result,
                )
            )   

        for subject_requirement in requirement.subject_requirements:

            subject_key = (
                subject_requirement.subject.strip().casefold()
            )

            student_result = student_results.get(subject_key)

            if (
                subject_requirement.minimum_grade is not None
                and requirement.credential_type != "WAEC"
            ):
                result = {
                    "status": "UNKNOWN",
                    "reason": (
                        "The minimum grade is not explicitly "
                        "identified as a WAEC requirement."
                    ),
                }
            else:
                result = match_subject_requirement(
                    student_result,
                    subject_requirement,
                )

            assessments.append(
                SubjectAssessmentResponse(
                    requirement_id=requirement.id,
                    subject_requirement_id=subject_requirement.id,
                    subject=subject_requirement.subject,
                    requirement_level=(
                        subject_requirement.requirement_level
                    ),
                    student_grade=(
                        student_result.grade
                        if student_result is not None
                        else None
                    ),
                    minimum_grade=subject_requirement.minimum_grade,
                    minimum_years=subject_requirement.minimum_years,
                    minimum_course_level=(
                        subject_requirement.minimum_course_level
                    ),
                    status=result["status"],
                    reason=result["reason"],
                    sources=sources,
                )
            )
    all_assessments = [
        *assessments,
        *aggregate_assessments,
    ]
    evaluated_status = calculate_program_status(all_assessments)

    # We have not established complete admission requirement
    # coverage for any program yet.
    academic_status = (
        "NOT_SATISFIED"
        if evaluated_status == "NOT_SATISFIED"
        else "UNKNOWN"
    )

    explanation = build_explanation(
        evaluated_status,
        all_assessments,
    )

    return ProgramRecommendationResponse(
        university_id=university.id,
        university_name=university.name,
        university_country=university.country,
        program_id=program.id,
        program_name=program.name,
        academic_status=academic_status,
        evaluated_requirements_status=evaluated_status,
        explanation=explanation,
        subject_assessments=assessments,
        requirements_complete=False,
        aggregate_assessments=aggregate_assessments,
    )


def generate_recommendations(
    db: Session,
    student: Student,
    intended_major: str | None = None,
    use_ai: bool = True,
):
    student_results = get_student_waec_results(
        db,
        student,
    )
    academic_results = [
        f"{result.subject}: {result.grade}"
        for result in student_results.values()
    ]

    query = (
        db.query(Program)
        .options(selectinload(Program.university))
        .join(University)
        .filter(University.country == "United States")
    )

    if intended_major:
        query = query.filter(
            Program.name.ilike(
                f"%{intended_major.strip()}%"
            )
        )

    programs = query.order_by(Program.id).all()

    recommendations = []

    for program in programs:
        recommendation = evaluate_program(
            db=db,
            student=student,
            university=program.university,
            program=program,
            student_results=student_results,
        )

        if use_ai:
            recommendation = enhance_recommendation(
                recommendation=recommendation,
                student_country=student.country,
                academic_results=academic_results,
            )

        recommendations.append(recommendation)

    status_priority = {
        "SATISFIED": 0,
        "UNKNOWN": 1,
        "NOT_SATISFIED": 2,
    }

    recommendations.sort(
        key=lambda recommendation: (
            status_priority[
                recommendation.evaluated_requirements_status
            ],
            not bool(recommendation.subject_assessments or recommendation.aggregate_assessments),
            recommendation.university_name,
        )
    )

    return RecommendationResponse(
        student_index=student.student_index,
        student_country=student.country,
        credential_type="WAEC",
        total_recommendations=len(recommendations),
        recommendations=recommendations,
    )