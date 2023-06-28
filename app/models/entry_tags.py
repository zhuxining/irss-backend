from datetime import datetime

import pymongo
from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel


class Tag(Document):
    name: str = Field(default="Default")
    path: str | None = None
    icon_type: str | None = None
    icon_value: str | None = None
    update_time: datetime

    owner_id: PydanticObjectId

    class Settings:
        name = "entry-tags"
        indexes = [
            IndexModel([("name", pymongo.ASCENDING)], unique=False),
            IndexModel([("path", pymongo.ASCENDING)], unique=False),
        ]
