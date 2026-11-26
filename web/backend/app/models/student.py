import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    student_index = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
        default=lambda: f"STU-{uuid.uuid4().hex[:8].upper()}",
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    country = Column(
        String,
        nullable=False,
    )

    education_level = Column(
        String,
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="student",
    )

    academic_credentials = relationship(
        "AcademicCredential",
        back_populates="student",
        cascade="all, delete-orphan",
    )