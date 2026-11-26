from app.services.admission_matcher import (
    WAEC_GRADE_RANK,
    meets_waec_minimum_grade,
)


def evaluate_aggregate_requirements(
    requirement,
    student_results: dict,
):
    assessments = []

    minimum_count = requirement.minimum_credit_count
    minimum_grade = requirement.minimum_credit_grade

    if minimum_count is not None or minimum_grade is not None:

        credit_count = None

        if (
            requirement.credential_type != "WAEC"
            or minimum_count is None
            or minimum_count <= 0
            or minimum_grade not in WAEC_GRADE_RANK
        ):
            status = "UNKNOWN"
            reason = (
                "The credit requirement does not have "
                "a valid, explicit WAEC threshold."
            )

        else:
            credit_count = sum(
                1
                for result in student_results.values()
                if meets_waec_minimum_grade(
                    result.grade,
                    minimum_grade,
                )
            )

            if credit_count >= minimum_count:
                status = "SATISFIED"
                reason = (
                    f"The student has {credit_count} recorded "
                    f"subjects graded {minimum_grade} or better, "
                    f"meeting the minimum of {minimum_count}."
                )
            else:
                status = "UNKNOWN"
                reason = (
                    f"Only {credit_count} qualifying subjects "
                    f"are recorded, compared with the required "
                    f"{minimum_count}. The completeness of the "
                    "student's results has not been established."
                )

        assessments.append({
            "requirement_type": "minimum_credits",
            "required_value": minimum_count,
            "student_value": credit_count,
            "minimum_grade": minimum_grade,
            "status": status,
            "reason": reason,
        })

    if requirement.minimum_gpa is not None:
        assessments.append({
            "requirement_type": "minimum_gpa",
            "required_value": requirement.minimum_gpa,
            "student_value": None,
            "gpa_scale": requirement.gpa_scale,
            "status": "UNKNOWN",
            "reason": (
                "A verified GPA on the required scale "
                "is not available. WAEC grades cannot "
                "automatically be converted to this GPA."
            ),
        })

    if requirement.minimum_percentage is not None:
        assessments.append({
            "requirement_type": "minimum_percentage",
            "required_value": requirement.minimum_percentage,
            "student_value": None,
            "status": "UNKNOWN",
            "reason": (
                "The student's secondary-school percentage "
                "average is not available. WAEC letter grades "
                "do not establish an overall percentage."
            ),
        })

    return assessments