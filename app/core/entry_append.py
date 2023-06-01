import asyncio
import time
from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException, status
from pydantic import HttpUrl

from app.common.response import resp, state
from app.crud.entries import c_entry, cm_entry
from app.models.entries import Entry
from app.schemas.entries import EntryParser, EntryUpdate


def should_update_feed() -> bool:
    return False


def should_update_entry() -> bool:
    return False


async def cm_entry(
    entryies: list[EntryParser], loop: asyncio.AbstractEventLoop
) -> None:
    asyncio.set_event_loop(loop)
    for entry in entryies:
        db_entry = Entry(**entry.dict())
        db_entry.create_time = datetime.utcnow()
        await Entry.insert_one(db_entry)


def get_feed_to_update():
    pass
