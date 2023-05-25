from datetime import datetime

import pymongo
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, HttpUrl
from pymongo import IndexModel


class Logo(BaseModel):
    url: HttpUrl
    # The default feed.logo : "url + /favicon.ico"
    is_default: bool = True
    is_choose: bool = True


class Feed(Document):
    url: HttpUrl
    updated: datetime | None = None
    title: str | None = None
    link: HttpUrl | None = None
    author: str | None = None
    subtitle: str | None = None
    # The feed type and version,rss or atom
    version: str | None = None

    view_layout: str | None = None
    display_title: str | None = None
    updates_enabled: bool = True
    logo: list[Logo] | None = None

    owner_id: PydanticObjectId | None = None
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: datetime | None = None
    last_exception: None = None

    class Settings:
        name = "feed"
        indexes = [
            IndexModel([("updated", pymongo.DESCENDING)], unique=False),
            IndexModel(
                [
                    ("title", pymongo.TEXT),
                    ("subtitle", pymongo.TEXT),
                    ("display_title", pymongo.TEXT),
                    ("author", pymongo.TEXT),
                ],
                name="text_index",
            ),
        ]
