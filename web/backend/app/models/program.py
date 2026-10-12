from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Program(Base):
    __tablename__ = "programs"

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

    name = Column(
        String,
        nullable=False,
        index=True,
    )

    university = relationship(
        "University",
        back_populates="programs",
    )

    admission_requirements = relationship(
        "AdmissionRequirement",
        back_populates="program",
        cascade="all, delete-orphan",
    )