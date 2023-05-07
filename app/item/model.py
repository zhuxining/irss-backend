from beanie import Document


class Item(Document):
    title: str
    description: str
    num: int
