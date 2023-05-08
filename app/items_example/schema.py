from pydantic import BaseModel
from typing import Set, Union, List
from app.api.api_v1.endpoints import item

from app.utils.response_format import ResponseModel


class Image(BaseModel):
    url: str
    name: str


class ItemBase(BaseModel):
    name: str
    description: str
    num: int
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[List[Image], None] = None


class ItemCreate(ItemBase):
    name: str
    description: str


class ItemUpdate(ItemBase):
    description: str
    description1: str


class Item(ItemBase):
    pass
