from langgraph.graph import StateGraph, START, END

from app.ai.workflows.state import RecommendationState

from app.ai.workflows.nodes import (
    generate_assessment,
    verify_node,
    revise_assessment,
    route_after_generation,
    route_after_verification,
)


def build_recommendation_graph():
    graph = StateGraph(RecommendationState)

    graph.add_node(
        "generate",
        generate_assessment,
    )

    graph.add_node(
        "verify",
        verify_node,
    )

    graph.add_node(
        "revise",
        revise_assessment,
    )

    graph.add_edge(START, "generate")

    graph.add_conditional_edges(
        "generate",
        route_after_generation,
        {
            "verify": "verify",
            "finish": END,
        },
    )

    graph.add_conditional_edges(
        "verify",
        route_after_verification,
        {
            "finish": END,
            "revise": "revise",
        },
    )

    graph.add_conditional_edges(
        "revise",
        route_after_generation,
        {
            "verify": "verify",
            "finish": END,
        },
    )

    return graph.compile()


recommendation_graph = build_recommendation_graph()


def run_recommendation_workflow(
    student_country: str,
    credential_type: str,
    academic_results: list[str],
    university: str,
    program: str,
    verified_requirements: str,
    expected_status: str,
):
    initial_state: RecommendationState = {
        "student_country": student_country,
        "credential_type": credential_type,
        "academic_results": academic_results,
        "university": university,
        "program": program,
        "verified_requirements": verified_requirements,
        "expected_status": expected_status,
        "initial_assessment": "",
        "assessment": "",
        "verified": False,
        "issues": [],
        "revisions": 0,
        "error": None,
    }

    return recommendation_graph.invoke(initial_state)