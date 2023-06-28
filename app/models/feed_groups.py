from datetime import datetime

import pymongo
from beanie import Document, PydanticObjectId
from pymongo import IndexModel

from app.models.feeds import Feed


class Group(Document):
    name: str
    icon_type: str | None = None
    icon_value: str | None = None
    update_time: datetime
    feed: list[Feed] | None = None

    owner_id: PydanticObjectId

    class Settings:
        name = "feed-groups"
        indexes = [
            IndexModel([("name", pymongo.ASCENDING)], unique=False),
            IndexModel([("owner_id", pymongo.ASCENDING)], unique=False),
        ]
