from beanie import init_beanie

from app.items_example.model import Item
from app.models.feeds import Feed
from app.models.users import User

from .database import db


async def init_db():
    await init_beanie(
        database=db,
        document_models=[
            User,
            Feed,
            Item,
        ],  # type: ignore
    )
