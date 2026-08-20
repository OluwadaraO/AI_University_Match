import uuid

from sqlalchemy import Column, Integer, String
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

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