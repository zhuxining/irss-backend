from fastapi import Depends
from shutil import which
from threading import get_ident
from app.models.feeds import Feed
from app.db.database import async_session_maker
from app import models, schemas
from app.db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def create_feed(feed: schemas.FeedCreate, db: AsyncSession):
    async with db.begin():
        db.add(Feed(**feed.dict()))


async def update_feed(feed_id: int, feed: schemas.FeedCreate, db: AsyncSession):
    async with db.begin():
        db.query(Feed).filter(Feed.id == feed_id).update(feed.dict())


async def delete_feed(feed_id: int, db: AsyncSession):
    async with db.begin():
        db.query(Feed).filter(Feed.id == feed_id).delete()


async def get_async_session() -> AsyncSession:
    async with get_async_session() as session:
        yield session
