from pydantic import BaseModel, constr, conint, Field


class ManCreate(BaseModel):
    name: str
    age: int
    mumber: int
    description: str | None
    home: str


class ManUpdate(BaseModel):
    name: constr(min_length=1, max_length=50) = None
    age: conint(ge=0, le=120) = None
