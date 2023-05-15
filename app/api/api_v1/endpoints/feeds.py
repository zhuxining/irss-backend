from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from app.crud.feeds import get_feeds
from app.models.feeds import Feed
from app.schemas.feeds import FeedBase, FeedTest

router = APIRouter()


@router.get("/feeds", response_model=List[Feed])
async def get_feeds():
    return await get_feeds()


# @router.post("/", response_model=Feed)
# async def create_feed(feed: FeedTest):
#     try:
#         db_feed = await Feed.insert(FeedTest)
#         return db_feed
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=e.json())


# @router.get("/", response_model=List[FeedTest])
# async def get_feeds():
#     users = await Feed.all().to_list()
#     return users
