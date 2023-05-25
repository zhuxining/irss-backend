from datetime import datetime
from typing import Any

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, HttpUrl
from pymongo import IndexModel

from app.models.entries import Content, Enclosures
from app.models.entry_tags import Tag


class EntryBase(BaseModel):
    feed_url: HttpUrl

    title: str | None = None
    link: HttpUrl
    author: str | None = None
    published: datetime | None = None
    summary: str | None = None
    content: list[Content] | None = None
    enclosures: list[Enclosures] | None = None


class EntryCreate(EntryBase):
    owner_id: PydanticObjectId | None = None


class EntryUpdate(EntryBase):
    is_read: bool = False
    read_modified: datetime | None = None
    read_later: bool = False
    read_later_modified: datetime | None = None
    is_hide: bool = False
    hide_modified: datetime | None = None

    is_star: bool = False
    star_modified: datetime | None = None
    tag: list[Tag] | None = None

    update_time: datetime | None = None
