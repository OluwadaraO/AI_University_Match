
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
    """Convert sourced database requirements into AI context."""

    if not requirements:
        return "NO VERIFIED REQUIREMENTS AVAILABLE"

    sections = []

    for requirement in requirements:
        lines = [
            f"Requirement ID: {requirement.id}",
            f"Requirement type: {requirement.requirement_type}",
            f"Applicant country: {requirement.applicant_country}",
            f"Credential type: {requirement.credential_type or 'General'}",
        ]

        for subject in requirement.subject_requirements:
            lines.extend([
                f"Subject: {subject.subject}",
                f"Requirement level: {subject.requirement_level}",
                f"Minimum grade: {subject.minimum_grade or 'Not specified'}",
                f"Minimum years: {subject.minimum_years if subject.minimum_years is not None else 'Not specified'}",
                f"Minimum course level: {subject.minimum_course_level or 'Not specified'}",
            ])

        for source in requirement.sources:
            lines.extend([
                f"Source title: {source.source_title}",
                f"Source URL: {source.source_url}",
                f"Verified date: {source.verified_date}",
            ])

        sections.append("\n".join(lines))

    return "\n\n---\n\n".join(sections)
