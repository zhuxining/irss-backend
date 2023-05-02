from pydantic import Field
from uuid import UUID, uuid4
from beanie import Document, Indexed


class Man(Document):
    # id: UUID = Field(default_factory=uuid4)
    name: str
    age: int
    mumber: int
    description: str
    home: str

    class Settings:
        neme = "man"
        Indexed = [
            "id",
            "name",
            "age",
            "mumber",
        ]
