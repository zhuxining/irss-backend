from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.common.response import resp, state
from app.models.entries import Entry
from app.schemas.entries import EntryCreate, EntryUpdate


async def c_entry(entry: EntryCreate) -> Entry:
    db_entry = Entry(**entry.dict())
    db_entry.create_time = datetime.utcnow()
    await Entry.insert_one(db_entry)
    return db_entry


async def r_entries() -> list[Entry]:
    db_entrys = await Entry.find_all().to_list()
    return db_entrys


async def r_entry(entry_id: PydanticObjectId) -> Entry:
    db_entry = await Entry.find_one({"_id": PydanticObjectId(entry_id)})
    if db_entry is None:
        raise state.DataNotFound
    return db_entry


async def u_entry(
    entry_id: PydanticObjectId,
    entry: EntryUpdate,
) -> Entry:
    await Entry.find_one({"_id": entry_id}).update_one(
        {"$set": {**entry.dict(), "update_time": datetime.utcnow()}}
    )
    return await r_entry(entry_id)


async def d_entry(entry_id: PydanticObjectId) -> None:
    await Entry.find_one({"_id": entry_id}).delete()


async def c_user_entry(entry: EntryCreate, owner_id: PydanticObjectId | None) -> Entry:
    db_entry = Entry(**entry.dict())
    db_entry.owner_id = owner_id
    db_entry.create_time = datetime.utcnow()
    await Entry.insert_one(db_entry)
    return db_entry


async def r_user_entries(user_id: PydanticObjectId | None) -> list[Entry]:
    db_entrys = await Entry.find({"owner_id": user_id}).to_list()
    return db_entrys


async def r_user_entry(
    entry_id: PydanticObjectId, user_id: PydanticObjectId | None
) -> Entry:
    db_entry = await Entry.find_one({"owner_id": user_id, "_id": entry_id})
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="entry not found"
        )
    return db_entry


async def u_user_entry(
    entry_id: PydanticObjectId,
    entry: EntryUpdate,
    update_by: PydanticObjectId | None,
) -> Entry:
    await Entry.find_one({"_id": entry_id}).update_one(
        {
            "$set": {
                **entry.dict(),
                "update_by": update_by,
                "update_time": datetime.utcnow(),
            }
        }
    )
    return await r_entry(entry_id)


async def d_user_entry(
    entry_id: PydanticObjectId, user_id: PydanticObjectId | None
) -> None:
    await Entry.find_one({"_id": entry_id, "owner_id": user_id}).delete()
