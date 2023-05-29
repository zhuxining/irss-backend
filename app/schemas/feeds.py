from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl

from app.models.feeds import Logo


class FeedBase(BaseModel):
    url: HttpUrl
    updated: datetime | None = None
    title: str | None = None
    link: HttpUrl | None = None
    author: str | None = None
    subtitle: str | None = None
    version: str | None = None


class FeedCreate(FeedBase):
    view_layout: str | None = None
    display_title: str | None = None
    updates_enabled: bool = True
    logo: list[Logo] | None = None

    owner_id: PydanticObjectId | None = None


class FeedUpdate(FeedBase):
    update_time: datetime | None = None


class FeedRead(FeedBase):
    pass
