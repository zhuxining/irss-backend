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
    create_by: PydanticObjectId | None
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_by: PydanticObjectId | None = None
    update_time: datetime | None = None

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
