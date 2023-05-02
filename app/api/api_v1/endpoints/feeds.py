from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

# from app.api.deps import get_db
# from app.crud import get_feed, get_feeds, create_user_feed

from app import models, schemas, crud

from app.db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("")
async def default():
    return {"message": "Hello World"}


# @router.get("/feeds/", response_model=List[schemas.Feed])
# def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     feeds = crud.get_feeds(db, skip=skip, limit=limit)
#     return feeds


# @router.get("/feeds/{feed_id}", response_model=schemas.Feed)
# def read_feed(feed_id: int, db: Session = Depends(get_db)):
#     db_feed = crud.get_feed(db, feed_id=feed_id)
#     if db_feed is None:
#         raise HTTPException(status_code=404, detail="Feed not found")
#     return db_feed


@router.post("/feeds")
async def create_feed_api(
    feed: schemas.FeedCreate, db: AsyncSession = Depends(get_async_session)
):
    await crud.create_feed(feed, db)
    return {"message": "Feed created successfully"}


@router.put("/feeds/{feed_id}")
async def update_feed_api(
    feed_id: int,
    feed: schemas.FeedCreate,
    db: AsyncSession = Depends(get_async_session),
):
    await crud.update_feed(feed_id, feed, db)
    return {"message": "Feed updated successfully"}


@router.delete("/feeds/{feed_id}")
async def delete_feed_api(feed_id: int, db: AsyncSession = Depends(get_async_session)):
    await crud.delete_feed(feed_id, db)
    return {"message": "Feed deleted successfully"}
