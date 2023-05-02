from pydantic import BaseModel


class Feed(BaseModel):
    id: int
    title: str
    description: str


class FeedCreate(BaseModel):
    title: str
    description: str


class FeedRead(BaseModel):
    id: int
    title: str
    description: str
