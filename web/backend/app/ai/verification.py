
from dataclasses import dataclass, field


@dataclass
class VerificationResult:
    is_valid: bool
    issues: list[str] = field(default_factory=list)


def verify_assessment(
    assessment: str,
    expected_status: str,
) -> VerificationResult:
    """
    Initial status consistency check.

    This is not yet full factual claim verification.
    """

    issues = []

    allowed_statuses = {
        "SATISFIED",
        "NOT_SATISFIED",
        "UNKNOWN",
    }

    if expected_status not in allowed_statuses:
        raise ValueError(
            f"Unexpected status: {expected_status}"
        )

    # Require an explicit status line so we can reliably
    # extract the model's eligibility assessment.
    import re

    match = re.search(
        r"(?im)^\s*(?:\*\*)?(?:Evaluation Status|Status)"
        r"(?:\*\*)?\s*:\s*(?:\*\*)?"
        r"(SATISFIED|NOT_SATISFIED|UNKNOWN)\b",
        assessment,
    )

    if not match:
        issues.append(
            "Missing explicit evaluation status. "
            "Use 'Evaluation Status: UNKNOWN', "
            "'SATISFIED', or 'NOT_SATISFIED'."
        )
    else:
        actual_status = match.group(1).upper()

        if actual_status != expected_status:
            issues.append(
                f"Status mismatch: expected {expected_status}, "
                f"but AI returned {actual_status}."
            )

    return VerificationResult(
        is_valid=len(issues) == 0,
        issues=issues,
    )
