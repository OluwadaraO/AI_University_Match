from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    email: EmailStr
    country: str
    education_level: str


class StudentResponse(BaseModel):
    id: int
    student_index: str
    email: EmailStr
    country: str
    education_level: str

    model_config = {
        "from_attributes": True
    }