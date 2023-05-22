from pydantic import BaseModel


class Image(BaseModel):
    url: str
    name: str


class ItemBase(BaseModel):
    name: str
    description: str
    num: int
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: list[Image] | None = None


class ItemCreate(ItemBase):
    name: str
    description: str


class ItemUpdate(ItemBase):
    description: str


class Item(ItemBase):
    pass


class ItemRead(BaseModel):
    name: str
    description: str
