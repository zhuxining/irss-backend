from datetime import datetime
from enum import Enum
import pymongo
from beanie import Document, PydanticObjectId
from pydantic import Field, HttpUrl
from pymongo import IndexModel


class ListLayout(str, Enum):
    a = "aaa"
    b = "bbb"


class ViewBrowser(str, Enum):
    a = "aaa"
    b = "bbb"


class Feed(Document):
    url: HttpUrl
    updated: datetime | None = None
    title: str | None = None
    link: HttpUrl | None = None
    author: str | None = None
    subtitle: str | None = None
    # The feed type and version,rss or atom
    version: str | None = None
    # The default feed.logo : "link + /favicon.ico"
    logo_url: str | None = None

    list_layout: ListLayout = ListLayout.a
    view_browser: ViewBrowser = ViewBrowser.a
    display_title: str | None = None
    updates_enabled: bool = True

    owner_id: PydanticObjectId | None = None
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: datetime | None = None
    newest_entry_pub_time: datetime
    last_parser_exception: None = None

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
