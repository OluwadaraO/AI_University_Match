from app.ai.baseline import get_baseline_assessment


def run_baseline_test():
    print("AI METHOD 1: BASIC LLM BASELINE")
    print("=" * 50)

    student_country = "Nigeria"
    credential_type = "WAEC"
    academic_results = [
        "Mathematics: A1"
    ]

    university = "University of Illinois Urbana-Champaign"
    program = "Computer Science"

    print(f"Student country: {student_country}")
    print(f"Credential: {credential_type}")
    print(f"Results: {academic_results}")
    print(f"University: {university}")
    print(f"Program: {program}")

    print("\nBASELINE AI RESPONSE")
    print("-" * 50)

    assessment = get_baseline_assessment(
        student_country=student_country,
        credential_type=credential_type,
        academic_results=academic_results,
        university=university,
        program=program,
    )

    print(assessment)


if __name__ == "__main__":
    run_baseline_test()