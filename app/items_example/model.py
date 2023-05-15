from datetime import datetime
from uuid import UUID, uuid4

import pymongo
from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel


class Item(Document):
    uid: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    num: int
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: list | None = None
    created_by: PydanticObjectId | None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: PydanticObjectId | None = None
    updated_at: datetime | None = None

    class Settings:
        name = "item"
        indexes = [
            IndexModel([("uid", pymongo.DESCENDING)], unique=True),
            IndexModel([("num", pymongo.ASCENDING)], unique=False),
            IndexModel([("name", pymongo.ASCENDING)], unique=True),
            IndexModel(
                [
                    ("name", pymongo.TEXT),
                    ("description", pymongo.TEXT),
                    ("tags", pymongo.TEXT),
                ],
                name="text_index",
            ),
        ]
