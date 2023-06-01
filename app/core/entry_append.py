import asyncio

from pydantic import HttpUrl

from app.common.response import resp, state
from app.crud.entries import c_entry
from app.models.entries import Entry
from app.schemas.entries import EntryParser, EntryUpdate


def should_update_feed() -> bool:
    return False


def should_update_entry() -> bool:
    return False


def get_entries_to_update(entries: list[EntryParser]):
    for entry in entries:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(c_entry(entry))


def get_feed_to_update():
    pass
