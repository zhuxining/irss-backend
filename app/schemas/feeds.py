from datetime import datetime


from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl

from app.models.feeds import ListLayout, ViewBrowser


class FeedParser(BaseModel):
    url: HttpUrl
    updated: datetime | None = None
    title: str
    link: HttpUrl
    author: str | None = None
    subtitle: str | None = None
    version: str
    logo_url: str


class FeedBase(FeedParser):
    display_title: str | None = None
    list_layout: ListLayout
    view_browser: ViewBrowser
    updates_enabled: bool = True


class FeedCreate(BaseModel):
    url: HttpUrl
    display_title: str | None = None


class FeedUpdate(BaseModel):
    display_title: str | None = None
    list_layout: ListLayout
    view_browser: ViewBrowser
    updates_enabled: bool = True
    logo_url: str
    update_time: datetime


class FeedRead(FeedBase):
    create_time: datetime
    update_time: datetime
    owner_id: PydanticObjectId
