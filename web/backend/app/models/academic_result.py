from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class AcademicResult(Base):
    __tablename__ = "academic_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    credential_id = Column(
        Integer,
        ForeignKey("academic_credentials.id"),
        nullable=False,
        index=True,
    )

    subject = Column(
        String,
        nullable=False,
    )

    grade = Column(
        String,
        nullable=False,
    )

    credential = relationship(
        "AcademicCredential",
        back_populates="results",
    )