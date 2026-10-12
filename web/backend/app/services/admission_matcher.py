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
    student_rank = WAEC_GRADE_RANK.get(student_grade.upper())
    minimum_rank = WAEC_GRADE_RANK.get(minimum_grade.upper())

    if student_rank is None or minimum_rank is None:
        return None

    return student_rank <= minimum_rank

def match_subject_requirement(student_result, requirement):
    if student_result is None:
        return {
            "status": "NOT_SATISFIED",
            "reason": (
                f"Student does not have a result for "
                f"{requirement.subject}."
            ),
        }

    # If the requirement depends on information that the student's
    # academic result does not contain, we cannot safely determine
    # whether the requirement is satisfied.
    if requirement.minimum_years is not None:
        return {
            "status": "UNKNOWN",
            "reason": (
                f"The requirement specifies at least "
                f"{requirement.minimum_years} years of "
                f"{requirement.subject}, but the student's academic "
                f"result does not include years of coursework."
            ),
        }

    if requirement.minimum_course_level is not None:
        return {
            "status": "UNKNOWN",
            "reason": (
                f"The requirement specifies a course level of "
                f"{requirement.minimum_course_level}, but the student's "
                f"academic result does not include course-level information."
            ),
        }

    # If the university publishes a WAEC minimum grade,
    # compare it directly with the student's WAEC grade.
    if requirement.minimum_grade is not None:
        grade_result = meets_waec_minimum_grade(
            student_result.grade,
            requirement.minimum_grade,
        )

        if grade_result is True:
            return {
                "status": "SATISFIED",
                "reason": (
                    f"The student's grade of {student_result.grade} "
                    f"meets the minimum grade of "
                    f"{requirement.minimum_grade}."
                ),
            }

        if grade_result is False:
            return {
                "status": "NOT_SATISFIED",
                "reason": (
                    f"The student's grade of {student_result.grade} "
                    f"does not meet the minimum grade of "
                    f"{requirement.minimum_grade}."
                ),
            }

        return {
            "status": "UNKNOWN",
            "reason": (
                "The student grade or minimum grade could not "
                "be interpreted as a valid WAEC grade."
            ),
        }

    return {
        "status": "UNKNOWN",
        "reason": (
            "There is not enough information to evaluate "
            "this requirement."
        ),
    }