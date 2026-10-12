from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class AdmissionSource(Base):
    __tablename__ = "admission_sources"

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

    source_url = Column(
        String,
        nullable=False,
    )

    source_title = Column(
        String,
        nullable=False,
    )

    verified_date = Column(
        Date,
        nullable=False,
    )

    admission_requirement = relationship(
        "AdmissionRequirement",
        back_populates="sources",
    )