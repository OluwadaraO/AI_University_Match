from app.ai.workflows.recommendation_graph import (
    run_recommendation_workflow,
)


def main():
    result = run_recommendation_workflow(
        student_country="Nigeria",
        credential_type="WAEC",
        academic_results=[
            "Mathematics: A1",
            "English Language: B2",
            "Physics: B3",
        ],
        university="University of Illinois Urbana-Champaign",
        program="Computer Science",
        verified_requirements=(
            "Mathematics is required. "
            "Minimum coursework duration: 3.5 years. "
            "Minimum course level: Trigonometry or higher."
        ),
        expected_status="UNKNOWN",
    )

    print("\nINITIAL ASSESSMENT:")
    print(result["initial_assessment"])

    print("\nFINAL ASSESSMENT:")
    print(result["assessment"])

    print("\nWORKFLOW RESULTS:")
    print("Verified:", result["verified"])
    print("Revisions:", result["revisions"])
    print("Issues:", result["issues"])
    print("Error:", result["error"])

    assert result["error"] is None
    assert result["verified"] is True
    assert result["revisions"] <= 2

    print("\nLangGraph workflow test passed!")


if __name__ == "__main__":
    main()