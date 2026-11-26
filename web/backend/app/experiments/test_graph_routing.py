from unittest.mock import patch

from app.ai.workflows.recommendation_graph import (
    run_recommendation_workflow,
)


def run_workflow():
    return run_recommendation_workflow(
        student_country="Nigeria",
        credential_type="WAEC",
        academic_results=["Mathematics: A1"],
        university="University of Illinois Urbana-Champaign",
        program="Computer Science",
        verified_requirements=(
            "Mathematics requires 3.5 years of coursework."
        ),
        expected_status="UNKNOWN",
    )


def test_successful_generation():
    with patch(
        "app.ai.workflows.nodes.generate_text",
        return_value="Evaluation Status: UNKNOWN",
    ) as mock_generate:

        result = run_workflow()

        assert result["verified"] is True
        assert result["revisions"] == 0
        assert mock_generate.call_count == 1

    print("PASS: Successful initial generation")


def test_revision_correction():
    with patch(
        "app.ai.workflows.nodes.generate_text",
        side_effect=[
            "Evaluation Status: SATISFIED",
            "Evaluation Status: UNKNOWN",
        ],
    ) as mock_generate:

        result = run_workflow()

        assert result["verified"] is True
        assert result["revisions"] == 1
        assert mock_generate.call_count == 2

    print("PASS: Incorrect assessment corrected")


def test_revision_limit():
    with patch(
        "app.ai.workflows.nodes.generate_text",
        return_value="Evaluation Status: SATISFIED",
    ) as mock_generate:

        result = run_workflow()

        assert result["verified"] is False
        assert result["revisions"] == 2
        assert mock_generate.call_count == 3

    print("PASS: Maximum revision limit enforced")


def test_api_failure():
    with patch(
        "app.ai.workflows.nodes.generate_text",
        side_effect=RuntimeError("Gemini unavailable"),
    ) as mock_generate:

        result = run_workflow()

        assert result["verified"] is False
        assert result["error"] is not None
        assert mock_generate.call_count == 1

    print("PASS: API failure handled")


def test_revision_api_failure():
    with patch(
        "app.ai.workflows.nodes.generate_text",
        side_effect=[
            "Evaluation Status: SATISFIED",
            RuntimeError("Gemini unavailable"),
        ],
    ) as mock_generate:

        result = run_workflow()

        assert result["verified"] is False
        assert result["error"] is not None
        assert mock_generate.call_count == 2

    print("PASS: API failure during revision handled")


if __name__ == "__main__":
    test_successful_generation()
    test_revision_correction()
    test_revision_limit()
    test_api_failure()
    test_revision_api_failure()

    print("\nAll 5 LangGraph routing tests passed!")