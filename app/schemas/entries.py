from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl

from app.models.entries import Content, Enclosures
from app.models.entry_tags import Tag


class EntryParser(BaseModel):
    feed_url: HttpUrl

    title: str | None = None
    link: HttpUrl
    author: str | None = None
    published: datetime | None = None
    summary: str | None = None
    content: list[Content] | None = None
    enclosures: list[Enclosures] | None = None


class EntryBase(EntryParser):
    is_read: bool = False
    read_modified: datetime | None = None
    read_later: bool = False
    read_later_modified: datetime | None = None
    is_hide: bool = False
    hide_modified: datetime | None = None

    is_star: bool = False
    star_modified: datetime | None = None
    tag: list[Tag] | None = None


class EntryCreate(BaseModel):
    pass


class EntryUpdate(BaseModel):
    is_read: bool = False
    read_later: bool = False
    is_hide: bool = False
    is_star: bool = False
    # tag: list[Tag] | None = None


class EntryRead(EntryBase):
    update_time: datetime | None = None
    owner_id: PydanticObjectId | None = None
