from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class University(Base):
    __tablename__ = "universities"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
        index=True,
    )

    country = Column(
        String,
        nullable=False,
        index=True,
    )

    programs = relationship(
        "Program",
        back_populates="university",
        cascade="all, delete-orphan",
    )

    admission_requirements = relationship(
        "AdmissionRequirement",
        back_populates="university",
        cascade="all, delete-orphan",
    )