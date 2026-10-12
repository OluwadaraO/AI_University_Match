from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class AdmissionSubjectRequirement(Base):
    __tablename__ = "admission_subject_requirements"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    admission_requirement_id = Column(
        Integer,
        ForeignKey("admission_requirements.id"),
        nullable=False,
        index=True,
    )

    subject = Column(
        String,
        nullable=False,
    )

    requirement_level = Column(
        String,
        nullable=False,
    )

    minimum_grade = Column(
        String,
        nullable=True,
    )

    minimum_years = Column(
        Float,
        nullable=True,
    )

    minimum_course_level = Column(
        String,
        nullable=True,
    )

    admission_requirement = relationship(
        "AdmissionRequirement",
        back_populates="subject_requirements",
    )