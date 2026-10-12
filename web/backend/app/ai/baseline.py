from app.ai.client import client


MODEL = "gemini-3.8-flash"


def get_baseline_assessment(
    student_country: str,
    credential_type: str,
    academic_results: list[str],
    university: str,
    program: str,
) -> str:

    results_text = "\n".join(academic_results)

    prompt = f"""
Student: {student_country}, {credential_type}

Academic results:
{results_text}

Applying to:
University: {university}
Program: {program}

Does this student appear to meet the academic admission requirements?
Briefly explain your reasoning.
"""

    response = client.interactions.create(
        model=MODEL,
        input=prompt,
    )

    if response.output_text is None:
        raise ValueError("Gemini returned no text response.")

    return response.output_text