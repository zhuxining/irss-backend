import asyncio
from datetime import datetime
from itertools import count
from pydantic import BaseModel

from app.core.feed_parser import parse_feed
from app.crud.feeds import r_feeds, c_feed
from app.crud.entries import c_entry, cm_entry
from app.models.entries import Entry
from app.models.feeds import Feed
from app.schemas.entries import EntryParser

# from app.common.scheduler.scheduler import scheduler


def should_update_feed() -> bool:
    return False


def should_update_entry() -> bool:
    return False


# async def cm_entry(entryies: list[EntryParser], loop: asyncio.AbstractEventLoop):
#     asyncio.set_event_loop(loop)
#     for entry in entryies:
#         db_entry = Entry(**entry.dict())
#         db_entry.create_time = datetime.utcnow()
#         await Entry.insert_one(db_entry)


class OutputFeed(BaseModel):
    urls: str
    count: int


async def get_feed_to_update():
    feed_url_list = await Feed.distinct("url")
    # print(feed_url_list)
    for feed_url in feed_url_list:
        # print(feed_url)
        feed, entries = await parse_feed(feed_url)
        for entry in entries:
            db_entry = Entry(**entry.dict())
            await Entry.insert_one(db_entry)
