from beanie import Document


class Feed(Document):
    title: str
    link: str | None
    description: str | None
