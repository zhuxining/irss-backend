from pydantic import BaseModel


class Feed(BaseModel):
    title: str
    link: str
    description: str
