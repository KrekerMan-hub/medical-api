from pydantic import BaseModel, Field, ConfigDict

class PatientCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    diagnosis: str = Field(min_length=1, max_length=500)


class PatientResponse(PatientCreate):
    id: int

class DiagnosisUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    diagnosis: str = Field(min_length=1, max_length=500)