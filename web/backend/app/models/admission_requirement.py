from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class AdmissionRequirement(Base):
    __tablename__ = "admission_requirements"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    university_id = Column(
        Integer,
        ForeignKey("universities.id"),
        nullable=False,
        index=True,
    )

    program_id = Column(
        Integer,
        ForeignKey("programs.id"),
        nullable=True,
        index=True,
    )

    applicant_country = Column(
        String,
        nullable=False,
        index=True,
    )

    credential_type = Column(
        String,
        nullable=True,
    )

    requirement_type = Column(
        String,
        nullable=False,
    )

    minimum_credit_count = Column(
    Integer,
    nullable=True,
)

    minimum_credit_grade = Column(
        String,
        nullable=True,
    )

    minimum_gpa = Column(
        Float,
        nullable=True,
    )

    gpa_scale = Column(
        Float,
        nullable=True,
    )

    minimum_percentage = Column(
        Float,
        nullable=True,
    )

    university = relationship(
        "University",
        back_populates="admission_requirements",
    )

    program = relationship(
        "Program",
        back_populates="admission_requirements",
    )

    subject_requirements = relationship(
        "AdmissionSubjectRequirement",
        back_populates="admission_requirement",
        cascade="all, delete-orphan",
    )   

    sources = relationship(
        "AdmissionSource",
        back_populates="admission_requirement",
        cascade="all, delete-orphan",
    )