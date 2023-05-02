from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test1.db"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()


# Define models
class User(BaseModel):
    id: int
    name: str
    # feeds: List[Feed] = []


class Feed(BaseModel):
    id: int
    title: str
    content: str
    user_id: int


# Define schemas
class UserCreate(BaseModel):
    name: str


class UserRead(BaseModel):
    id: int
    name: str
    feeds: List[Feed]


class FeedCreate(BaseModel):
    title: str
    content: str
    user_id: int


class FeedRead(BaseModel):
    id: int
    title: str
    content: str
    user_id: int


# Define CRUD operations
async def create_user(user: UserCreate, db: AsyncSession):
    async with db.begin():
        db.add(User(**user.dict()))


async def read_user(user_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    return UserRead(
        **user.dict(), feeds=[FeedRead(**feed.dict()) for feed in user.feeds]
    )


async def create_feed(feed: FeedCreate, db: AsyncSession):
    async with db.begin():
        db.add(Feed(**feed.dict()))


async def update_feed(feed_id: int, feed: FeedCreate, db: AsyncSession):
    async with db.begin():
        db.query(Feed).filter(Feed.id == feed_id).update(feed.dict())


async def delete_feed(feed_id: int, db: AsyncSession):
    async with db.begin():
        db.query(Feed).filter(Feed.id == feed_id).delete()


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# Define API endpoints
@app.post("/users")
async def create_user_api(
    user: UserCreate, db: AsyncSession = Depends(get_async_session)
):
    await create_user(user, db)
    return {"message": "User created successfully"}


@app.get("/users/{user_id}")
async def read_user_api(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await read_user(user_id, db)
    return {"data": user}


@app.post("/feeds")
async def create_feed_api(
    feed: FeedCreate, db: AsyncSession = Depends(get_async_session)
):
    await create_feed(feed, db)
    return {"message": "Feed created successfully"}


@app.put("/feeds/{feed_id}")
async def update_feed_api(
    feed_id: int, feed: FeedCreate, db: AsyncSession = Depends(get_async_session)
):
    await update_feed(feed_id, feed, db)
    return {"message": "Feed updated successfully"}


@app.delete("/feeds/{feed_id}")
async def delete_feed_api(feed_id: int, db: AsyncSession = Depends(get_async_session)):
    await delete_feed(feed_id, db)
    return {"message": "Feed deleted successfully"}
