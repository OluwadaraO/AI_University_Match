
from pydantic import BaseModel, EmailStr, field_validator


class StudentAcademicBackground(BaseModel):
    education_level: str

    @field_validator("education_level")
    @classmethod
    def validate_education_level(cls, education_level: str):
        education_level = education_level.strip().lower()

        supported_levels = {
            "ss1": "SS1",
            "ss2": "SS2",
            "ss3": "SS3",
            "graduated": "Graduated",
        }

        if education_level not in supported_levels:
            raise ValueError(
                "Unsupported education level. "
                "Supported levels: SS1, SS2, SS3, Graduated"
            )

        return supported_levels[education_level]


class StudentCreate(StudentAcademicBackground):
    country: str

    @field_validator("country")
    @classmethod
    def validate_country(cls, country: str):
        country = country.strip().lower()

        supported_countries = {
            "nigeria": "Nigeria",
        }

        if country not in supported_countries:
            raise ValueError(
                "Unsupported country. Currently supported countries: Nigeria"
            )

        return supported_countries[country]


class StudentUpdate(StudentAcademicBackground):
    model_config = {
        "extra": "forbid"
    }


class StudentResponse(BaseModel):
    id: int
    student_index: str
    email: EmailStr
    country: str
    education_level: str

    model_config = {
        "from_attributes": True
    }
