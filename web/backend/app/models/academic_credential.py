from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AcademicCredential(Base):
    __tablename__ = "academic_credentials"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        index=True,
    )

    country = Column(
        String,
        nullable=False,
    )

    credential_type = Column(
        String,
        nullable=False,
    )

    student = relationship(
        "Student",
        back_populates="academic_credentials",
    )

    results = relationship(
        "AcademicResult",
        back_populates="credential",
        cascade="all, delete-orphan",
    )