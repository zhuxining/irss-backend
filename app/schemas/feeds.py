from datetime import datetime
from enum import Enum

from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl

from app.models.feeds import Logo


class ListLayout(str, Enum):
    a = "a"
    b = "b"


class FeedBase(BaseModel):
    url: HttpUrl
    updated: datetime | None = None
    title: str | None = None
    link: HttpUrl | None = None
    author: str | None = None
    subtitle: str | None = None
    version: str | None = None


class FeedBaseCreate(BaseModel):
    url: HttpUrl
    display_title: str | None = None
    list_layout: ListLayout = ListLayout.a


class FeedCreate(FeedBase):
    url: HttpUrl
    display_title: str | None = None
    list_layout: ListLayout = ListLayout.a
    view_browser: str | None = None
    updates_enabled: bool = True
    logo: list[Logo] | None = None

    owner_id: PydanticObjectId | None = None


class FeedUpdate(FeedBase):
    list_layout: ListLayout
    view_browser: str | None = None
    display_title: str | None = None
    updates_enabled: bool = True
    logo: list[Logo] | None = None
    update_time: datetime | None = None


class FeedRead(FeedBase):
    list_layout: ListLayout
    view_browser: str | None = None
    display_title: str | None = None
    updates_enabled: bool = True
    logo: list[Logo] | None = None

    update_time: datetime | None = None
    owner_id: PydanticObjectId | None = None
