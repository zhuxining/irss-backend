from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str
    num: int


class ItemCreate(ItemBase):
    title: str
    description: str


class ItemUpdate(ItemBase):
    description: str
    description1: str


class Item(ItemBase):
    pass
