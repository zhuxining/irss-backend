from app.models.feeds import Feed
from app.schemas.feeds import FeedBase

from typing import List
from fastapi import HTTPException


async def get_feeds() -> List[Feed]:
    feeds = await Feed.all().to_list()
    return feeds
