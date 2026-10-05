from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.database import Base


class AcademicSubject(Base):
    __tablename__ = "academic_subjects"

    id = Column(Integer, primary_key=True, index=True)

    country = Column(
        String,
        nullable=False,
        index=True,
    )

    credential_type = Column(
        String,
        nullable=False,
        index=True,
    )

    subject_name = Column(
        String,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "country",
            "credential_type",
            "subject_name",
            name="uq_academic_subject",
        ),
    )