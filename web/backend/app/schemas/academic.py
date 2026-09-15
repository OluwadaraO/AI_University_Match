from pydantic import BaseModel


class AcademicResultCreate(BaseModel):
    subject: str
    grade: str


class AcademicResultResponse(BaseModel):
    id: int
    subject: str
    grade: str

    model_config = {
        "from_attributes": True
    }


class AcademicCredentialCreate(BaseModel):
    credential_type: str
    results: list[AcademicResultCreate]


class AcademicCredentialResponse(BaseModel):
    id: int
    student_id: int
    country: str
    credential_type: str
    results: list[AcademicResultResponse]

    model_config = {
        "from_attributes": True
    }