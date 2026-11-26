WAEC_GRADE_RANK = {
    "A1": 1,
    "B2": 2,
    "B3": 3,
    "C4": 4,
    "C5": 5,
    "C6": 6,
    "D7": 7,
    "E8": 8,
    "F9": 9,
}


def meets_waec_minimum_grade(student_grade, minimum_grade):
    if not student_grade or not minimum_grade:
        return None

    student_rank = WAEC_GRADE_RANK.get(
        student_grade.strip().upper()
    )
    minimum_rank = WAEC_GRADE_RANK.get(
        minimum_grade.strip().upper()
    )

    if student_rank is None or minimum_rank is None:
        return None

    return student_rank <= minimum_rank


def match_subject_requirement(student_result, requirement):
    if student_result is None:
        return {
            "status": "UNKNOWN",
            "reason": (
                f"No academic result was provided for "
                f"{requirement.subject}."
            ),
        }

    checks = []

    if requirement.minimum_grade is not None:
        grade_result = meets_waec_minimum_grade(
            student_result.grade,
            requirement.minimum_grade,
        )

        if grade_result is True:
            checks.append({
                "status": "SATISFIED",
                "reason": (
                    f"Grade {student_result.grade} meets "
                    f"the minimum grade of "
                    f"{requirement.minimum_grade}."
                ),
            })

        elif grade_result is False:
            checks.append({
                "status": "NOT_SATISFIED",
                "reason": (
                    f"Grade {student_result.grade} does not "
                    f"meet the minimum grade of "
                    f"{requirement.minimum_grade}."
                ),
            })

        else:
            checks.append({
                "status": "UNKNOWN",
                "reason": "Unable to compare the WAEC grades.",
            })

    if requirement.minimum_years is not None:
        checks.append({
            "status": "UNKNOWN",
            "reason": (
                f"The requirement specifies at least "
                f"{requirement.minimum_years} years of "
                f"{requirement.subject}, but coursework "
                f"duration is not available."
            ),
        })

    if requirement.minimum_course_level is not None:
        checks.append({
            "status": "UNKNOWN",
            "reason": (
                f"The requirement specifies "
                f"{requirement.minimum_course_level}, "
                f"but course-level information is not available."
            ),
        })

    if not checks:
        return {
            "status": "UNKNOWN",
            "reason": "No evaluable admission criteria are available.",
        }

    statuses = [check["status"] for check in checks]

    if "NOT_SATISFIED" in statuses:
        overall_status = "NOT_SATISFIED"
    elif "UNKNOWN" in statuses:
        overall_status = "UNKNOWN"
    else:
        overall_status = "SATISFIED"

    return {
        "status": overall_status,
        "reason": " ".join(
            check["reason"] for check in checks
        ),
        "checks": checks,
    }