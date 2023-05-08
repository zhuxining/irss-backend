from beanie import Document
from typing import Any, Set, Union
from uuid import UUID, uuid4
from pydantic import Field


class Item(Document):
    uid: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    num: int
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Any = None
