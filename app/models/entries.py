from datetime import datetime
from typing import Any

import pymongo
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import IndexModel

from app.models.entry_tags import Tag
from app.models.feeds import Feed


class Content(BaseModel):
    type: str
    language: str | None = None
    base: str | None = None
    value: str


class Enclosures(BaseModel):
    href: str | None = None
    length: str | None = None
    type: str | None = None


class Entry(Document):
    feed_id: PydanticObjectId
    feed_url: str

    title: str | None = None
    link: str
    author: str | None = None
    published: datetime | None = None
    summary: str | None = None
    content: list[Content] | None = None
    enclosures: list[Enclosures] | None = None

    is_read: bool = False
    read_modified: datetime | None = None
    read_later: bool = False
    read_later_modified: datetime | None = None
    is_hide: bool = False
    hide_modified: datetime | None = None

    is_star: bool = False
    star_modified: datetime | None = None
    # start then tags, unstart can clear tags
    tag: list[Tag] | None = None

    owner_id: PydanticObjectId | None = None
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: datetime | None = None

    # The URL of the original feed of the entry.
    original_feed_url: str | None = None

    class Settings:
        name = "entries"
        indexes = [
            IndexModel([("published", pymongo.DESCENDING)], unique=False),
            IndexModel(
                [
                    ("title", pymongo.TEXT),
                    ("summary", pymongo.TEXT),
                    ("author", pymongo.TEXT),
                    ("tag", pymongo.TEXT),
                ],
                name="text_index",
            ),
        ]
