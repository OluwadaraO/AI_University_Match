from app.ai.client import client

MODEL = "gemini-3.8-flash"


def get_grounded_assessment(
    student_country: str,
    credential_type: str,
    academic_results: list[str],
    university: str,
    program: str,
    verified_requirements: str,
) -> str:

    results_text = "\n".join(academic_results)

    prompt = f"""
You are evaluating a student's academic preparation for a university program.

STUDENT:
Country: {student_country}
Credential: {credential_type}
Academic results:
{results_text}

UNIVERSITY:
{university}
Program: {program}

VERIFIED ADMISSION REQUIREMENTS:
{verified_requirements}

Instructions:
- Use only the verified requirements provided above.
- Do not invent additional admission requirements.
- Do not assume that WAEC grades are equivalent to US coursework years.
- If the available information is insufficient, explicitly say UNKNOWN.
- Explain which requirements can and cannot be verified.
- Do not confuse academic matching with an admission guarantee.

Provide a brief assessment.
"""

    response = client.interactions.create(
        model=MODEL,
        input=prompt,
    )

    if response.output_text is None:
        raise ValueError("Gemini returned no text response.")

    return response.output_text