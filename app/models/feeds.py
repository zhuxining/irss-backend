from datetime import datetime
from uuid import UUID, uuid4

import pymongo
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from pymongo import IndexModel


class Logo(BaseModel):
    url: str
    # The default feed.logo : "url + /favicon.ico"
    is_default: bool = True

    is_choose: bool = True


class Feed(Document):
    uid: UUID = Field(default_factory=uuid4)

    #: The URL of the feed.
    url: str

    #: The date the feed was last updated, according to the feed.
    updated: datetime | None = None

    #: The title of the feed.
    title: str | None = None

    #: The URL of a page associated with the feed.
    link: str | None = None

    #: The author of the feed.
    author: str | None = None

    #: A description or subtitle for the feed.

    subtitle: str | None = None

    #: The feed type and version.

    version: str | None = None

    #: User-defined feed title.
    user_title: str | None = None

    # user object

    added_by: object

    # added is required, but we want it after feed data; the cast is for mypy.

    #: The date when the feed was added.

    added: datetime

    #: The date when the feed was last retrieved by reader.

    last_updated: datetime = Field(default_factory=datetime.now)

    #: If a :ešc:`ParseError` happend during the last update, its cause.

    last_exception: None = None

    #: Whether updates are enabled for this feed.

    updates_enabled: bool = True

    logo: list[Logo] | None = None

    class Settings:
        name = "feed"
        indexes = [
            IndexModel([("uid", pymongo.DESCENDING)], unique=True),
            IndexModel([("user_title", pymongo.ASCENDING)], unique=False),
            IndexModel([("title", pymongo.ASCENDING)], unique=False),
            IndexModel(
                [
                    ("title", pymongo.TEXT),
                    ("subtitle", pymongo.TEXT),
                    ("user_title", pymongo.TEXT),
                    ("author", pymongo.TEXT),
                ],
                name="text_index",
            ),
        ]
