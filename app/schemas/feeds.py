from pydantic import BaseModel


class FeedBase(BaseModel):
    title: str
    link: str
    description: str


class FeedTest(BaseModel):
    title: str
