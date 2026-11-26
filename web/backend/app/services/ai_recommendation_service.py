import json
import logging

from app.schemas.recommendation import (
    ProgramRecommendationResponse,
)


logger = logging.getLogger(__name__)


def enhance_recommendation(
    recommendation: ProgramRecommendationResponse,
    student_country: str,
    academic_results: list[str],
) -> ProgramRecommendationResponse:

    if not (
        recommendation.subject_assessments
        or recommendation.aggregate_assessments
    ):
        return recommendation

    subject_evidence = [
        assessment.model_dump(mode="json")
        for assessment in recommendation.subject_assessments
    ]

    aggregate_evidence = [
        assessment.model_dump(mode="json")
        for assessment in recommendation.aggregate_assessments
    ]

    verified_requirements = json.dumps(
        {
            "requirements_complete": (
                recommendation.requirements_complete
            ),
            "academic_status": recommendation.academic_status,
            "evaluated_requirements_status": (
                recommendation.evaluated_requirements_status
            ),
            "subject_assessments": subject_evidence,
            "aggregate_assessments": aggregate_evidence,
        },
        indent=2,
    )

    try:
        from app.ai.workflows.recommendation_graph import (
            run_recommendation_workflow,
        )

        result = run_recommendation_workflow(
            student_country=student_country,
            credential_type="WAEC",
            academic_results=academic_results,
            university=recommendation.university_name,
            program=recommendation.program_name,
            verified_requirements=verified_requirements,
            expected_status=(
                recommendation.evaluated_requirements_status
            ),
        )

        if result["error"]:
            logger.warning(
                "LangGraph workflow failed: %s",
                result["error"],
            )
            return recommendation

        if not result["verified"]:
            logger.warning(
                "AI verification failed for program %s: %s",
                recommendation.program_id,
                result["issues"],
            )
            return recommendation

        recommendation.ai_generated = True
        recommendation.ai_verified = True
        recommendation.ai_assessment = result["assessment"]
        recommendation.ai_revisions = result["revisions"]

        logger.info(
            "LangGraph workflow completed for program %s "
            "after %s revisions.",
            recommendation.program_id,
            result["revisions"],
        )

    except Exception:
        logger.exception(
            "LangGraph recommendation failed for program %s. "
            "Using deterministic assessment.",
            recommendation.program_id,
        )

    return recommendation