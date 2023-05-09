from beanie import Document, Indexed
from typing import Any, Set, Union
from uuid import UUID, uuid4
from pydantic import Field
import pymongo
from pymongo import IndexModel


class Item(Document):
    uid: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    num: int
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Any = None

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
