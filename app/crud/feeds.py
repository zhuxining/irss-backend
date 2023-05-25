from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.common.response import resp, state
from app.models.feeds import Feed
from app.schemas.feeds import FeedBase, FeedCreate


async def create_feed(item: FeedCreate) -> Feed:
    db_feed = Feed(**item.dict())
    await Feed.insert_one(db_feed)
    return db_feed
