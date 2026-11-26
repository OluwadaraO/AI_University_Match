
from sqlalchemy.orm import Session, selectinload

from app.models import AdmissionRequirement


def get_verified_requirements(
    db: Session,
    university_id: int,
    program_id: int,
    applicant_country: str,
    credential_type: str,
) -> list[AdmissionRequirement]:
    """Retrieve sourced admission requirements for a program."""

    requirements = (
        db.query(AdmissionRequirement)
        .options(
            selectinload(
                AdmissionRequirement.subject_requirements
            ),
            selectinload(AdmissionRequirement.sources),
        )
        .filter(
            AdmissionRequirement.university_id == university_id,
            AdmissionRequirement.applicant_country == applicant_country,
            (
                (AdmissionRequirement.program_id == program_id)
                | (AdmissionRequirement.program_id.is_(None))
            ),
            (
                (AdmissionRequirement.credential_type == credential_type)
                | (AdmissionRequirement.credential_type.is_(None))
            ),
        )
        .all()
    )

    # Exclude requirements without recorded sources.
    return [
        requirement
        for requirement in requirements
        if requirement.sources
    ]


def format_requirements_for_ai(
    requirements: list[AdmissionRequirement],
) -> str:

    if not requirements:
        return "NO VERIFIED REQUIREMENTS AVAILABLE"

    sections = []

    for requirement in requirements:
        lines = [
            f"Requirement ID: {requirement.id}",
            f"Requirement type: {requirement.requirement_type}",
            f"Applicant country: {requirement.applicant_country}",
            f"Credential type: {requirement.credential_type or 'General'}",
            f"Minimum credits: {requirement.minimum_credit_count}",
            f"Minimum credit grade: {requirement.minimum_credit_grade}",
            f"Minimum GPA: {requirement.minimum_gpa}",
            f"GPA scale: {requirement.gpa_scale}",
            f"Minimum percentage: {requirement.minimum_percentage}",
        ]

        for subject in requirement.subject_requirements:
            lines.extend([
                f"Subject: {subject.subject}",
                f"Requirement level: {subject.requirement_level}",
                f"Minimum grade: {subject.minimum_grade}",
                f"Minimum years: {subject.minimum_years}",
                f"Minimum course level: {subject.minimum_course_level}",
            ])

        for source in requirement.sources:
            lines.extend([
                f"Source title: {source.source_title}",
                f"Source URL: {source.source_url}",
                f"Verified date: {source.verified_date}",
                f"Evidence: {source.evidence_text}",
                f"Admission cycle: {source.admission_cycle}",
            ])

        sections.append("\n".join(lines))

    return "\n\n---\n\n".join(sections)