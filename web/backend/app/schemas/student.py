from pydantic import BaseModel, EmailStr, field_validator

class StudentCreate(BaseModel):
    email: EmailStr
    country: str
    education_level: str

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


class StudentResponse(BaseModel):
    id: int
    student_index: str
    email: EmailStr
    country: str
    education_level: str

    model_config = {
        "from_attributes": True
    }