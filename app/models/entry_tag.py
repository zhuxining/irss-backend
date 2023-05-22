from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Tag(Document):
    name: str
    parent_id: PydanticObjectId | None = None
    children: list[PydanticObjectId] = Field(default=[])
