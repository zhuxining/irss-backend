from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.common.response import resp, state
from app.models.feeds import Feed
from app.schemas.feeds import FeedBase, FeedCreate, FeedUpdate


async def c_feed(feed: FeedCreate) -> Feed:
    db_feed = Feed(**feed.dict())
    db_feed.create_time = datetime.utcnow()
    await Feed.insert_one(db_feed)
    return db_feed


async def r_feeds() -> list[Feed]:
    db_feed = await Feed.find_all().to_list()
    return db_feed


async def r_feed(feed_id: PydanticObjectId) -> Feed:
    db_feed = await Feed.find_one({"_id": PydanticObjectId(feed_id)})
    if db_feed is None:
        raise ValueError
    return db_feed


async def u_feed(
    feed_id: PydanticObjectId,
    feed: FeedUpdate,
) -> Feed:
    await Feed.find_one({"_id": feed_id}).update_one(
        {"$set": {**feed.dict(), "update_time": datetime.utcnow()}}
    )
    return await r_feed(feed_id)


async def d_feed(feed_id: PydanticObjectId) -> None:
    await Feed.find_one({"_id": feed_id}).delete()


async def c_user_feed(feed: FeedCreate, owner_id: PydanticObjectId | None) -> Feed:
    db_feed = Feed(**feed.dict())
    db_feed.owner_id = owner_id
    db_feed.create_time = datetime.utcnow()
    await Feed.insert_one(db_feed)
    return db_feed


async def r_user_feeds(user_id: PydanticObjectId | None) -> list[Feed]:
    db_feeds = await Feed.find({"owner_id": user_id}).to_list()
    return db_feeds


async def r_user_feed(
    feed_id: PydanticObjectId, user_id: PydanticObjectId | None
) -> Feed:
    db_feed = await Feed.find_one({"owner_id": user_id, "_id": feed_id})
    if db_feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="feed not found"
        )
    return db_feed


async def u_user_feed(
    feed_id: PydanticObjectId,
    feed: FeedUpdate,
    update_by: PydanticObjectId | None,
) -> Feed:
    await Feed.find_one({"_id": feed_id}).update_one(
        {
            "$set": {
                **feed.dict(),
                "update_by": update_by,
                "update_time": datetime.utcnow(),
            }
        }
    )
    return await r_feed(feed_id)


async def d_user_feed(
    feed_id: PydanticObjectId, user_id: PydanticObjectId | None
) -> None:
    await Feed.find_one({"_id": feed_id, "owner_id": user_id}).delete()
