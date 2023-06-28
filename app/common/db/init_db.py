from beanie import init_beanie

from app.items_example.model import Item
from app.models import entries, entry_tags, feed_groups, feeds, users

from .database import db


async def init_db() -> None:
    await init_beanie(
        database=db,
        document_models=[
            users.User,
            Item,
            feeds.Feed,
            feed_groups.Group,
            entries.Entry,
            entry_tags.Tag,
        ],
    )
