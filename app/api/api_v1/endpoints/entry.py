from datetime import datetime

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import Response
from pydantic import Json

from app.common.response import resp, state
from app.core.feed_parser import parse_feed
from app.core.users import current_active_user
from app.crud.entries import c_entry
from app.models.entries import Entry
from app.models.users import User
from app.schemas.entries import EntryBase, EntryCreate, EntryUpdate
from app.utils.tools_func import paginated_find

router = APIRouter()


@router.get("/test/test2")
async def get_table_list_fail() -> Response:
    db_data = await Entry.find({"name": {"$regex": "str"}}).to_list()
    return resp.result(state.Ok, data=db_data)


@router.post("/", response_model=Entry)
async def create_entry(entry: EntryCreate) -> Response:
    """
    Create a new entry.
    """
    db_data = await c_entry(entry)
    return resp.result(state.Ok, data=db_data)


@router.get("/", response_model=list[Entry], response_description="list of entries")
async def list_entries(
    id: str = Query(default=None, description="mongodb ObjectId"),
    name: str = Query(default=None, max_length=50, description="fuzzy"),
    description: str = Query(default=None, max_length=50, description="fuzzy"),
    range_create_time: Json = Query(
        default=None,
        example={
            "start_time": "2000-01-01T00:00:00.000000",
            "end_time": "2100-01-01T00:00:00.000000",
        },
        description="json",
    ),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
) -> Response:
    """
    Get a list of entries by filters and pagination.
    """
    # Use the correct sorting order for descending order.

    filters = {}
    if id:
        filters["_id"] = PydanticObjectId(id)
    if name:
        filters["name"] = {"$regex": name}
    if description:
        filters["description"] = {"$regex": description}
    if range_create_time:
        start = datetime.fromisoformat(range_create_time["start_time"])
        end = datetime.fromisoformat(range_create_time["end_time"])

        # Use $gt and $lt instead of $gte and $lte to exclude the start and end times.
        filters["create_time"] = {
            "$gte": start,
            "$lte": end,
        }

    db_data = await paginated_find(Entry, filters, current, page_size, sort)

    return resp.result(state.Ok, data=db_data)


@router.get("/{entry_id}/", response_model=Entry)
async def get_entry(entry_id: PydanticObjectId) -> Response:
    """
    Get an entry by ID.
    """
    db_data = await Entry.find_one({"_id": entry_id})

    # Return a 404 error if the entry is not found.
    if db_data is None:
        return resp.result(state.DataNotFound)
    return resp.result(state.Ok, data=db_data)


@router.put("/{entry_id}/", response_model=Entry)
async def update_entry(entry_id: PydanticObjectId, entry: EntryUpdate) -> Response:
    """
    Update an entry by ID.
    """
    # Set the update_time field to the current time before updating in the database.
    db_data = await Entry.find_one({"_id": entry_id}).update_one(
        {"$set": {**entry.dict(), "update_time": datetime.utcnow()}}
    )
    db_result = await Entry.find_one({"_id": entry_id})
    return resp.result(state.Ok, data=db_result)


@router.delete("/{entry_id}/", response_model={})
async def delete_entry(entry_id: PydanticObjectId) -> Response:
    """
    delete by id
    """
    # annotating
    await Entry.find_one({"_id": entry_id}).delete()
    return resp.result(state.Ok, data={})


@router.get("/search/", response_model=list[Entry])
async def search_entries(
    q: str = Query(default=None, max_length=50, description="fuzzy:name、description"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
) -> Response:
    """
    get by fuzzy query then paged
    """
    # annotating
    filters = {}
    if q:
        filters = {"$or": [{"title": {"$regex": q}}, {"summary": {"$regex": q}}]}

    db_data = await paginated_find(Entry, filters, current, page_size, sort)

    return resp.result(state.Ok, data=db_data)


@router.post("/query/", response_model=list[Entry])
async def query_entries(
    filters: dict = Body(default=None, example={"name": "string"}, description="query"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
) -> Response:
    """
    post filters for query then paged
    """
    # annotating
    db_data = await paginated_find(Entry, filters, current, page_size, sort)
    return resp.result(state.Ok, data=db_data)


@router.post("/user-entry", response_model=Entry)
async def create_user_entry(
    entry: EntryCreate, user: User = Depends(current_active_user)
) -> Response:
    """
    create a new
    """
    # annotating
    db_entry = Entry(**entry.dict())
    db_entry.owner_id = user.id
    db_entry.create_time = datetime.utcnow()
    db_data = await Entry.insert_one(db_entry)
    return resp.result(state.Ok, data=db_data)


@router.get("/user-entries/", response_model=Entry)
async def list_user_entries(
    id: str = Query(default=None, description="mongodb ObjectId"),
    name: str = Query(default=None, max_length=50, description="fuzzy"),
    description: str = Query(default=None, max_length=50, description="fuzzy"),
    range_create_time: Json = Query(
        default=None,
        example={
            "start_time": "2000-01-01T00:00:00.000000",
            "end_time": "2100-01-01T00:00:00.000000",
        },
        description="json",
    ),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
    user: User = Depends(current_active_user),
) -> Response:
    """
    get list by filters and current_active_user then paged
    """
    # annotating

    filters = {}
    if id:
        filters["_id"] = PydanticObjectId(id)
    if name:
        filters["name"] = {"$regex": name}
    if description:
        filters["description"] = {"$regex": description}
    if range_create_time:
        start = datetime.fromisoformat(range_create_time["start_time"])
        end = datetime.fromisoformat(range_create_time["end_time"])
        filters["create_time"] = {
            "$gte": start,
            "$lte": end,
        }

    filters = {**filters, "owner_id": user.id}
    db_data = await paginated_find(Entry, filters, current, page_size, sort)
    return resp.result(state.Ok, data=db_data)


@router.get("/user-entry/{entry_id}/", response_model=Entry)
async def get_user_entry(
    entry_id: PydanticObjectId, user: User = Depends(current_active_user)
) -> Response:
    """
    get by id and current_user
    """
    # annotating
    db_data = await Entry.find_one({"owner_id": user.id, "_id": entry_id})
    return resp.result(state.Ok, data=db_data)


@router.put("/user-entry/{entry_id}/", response_model=Entry)
async def update_user_entry(
    entry_id: PydanticObjectId,
    entry: EntryUpdate,
    user: User = Depends(current_active_user),
) -> Response:
    """
    put by id
    """
    # annotating
    db_data = await Entry.find_one({"_id": entry_id}).update_one(
        {
            "$set": {
                **entry.dict(),
                "update_by": user.id,
                "update_time": datetime.utcnow(),
            }
        }
    )
    db_result = await Entry.find_one({"_id": entry_id})
    return resp.result(state.Ok, data=db_result)


@router.delete("/user-entry/{entry_id}/", response_model={})
async def delete_user_entry(
    entry_id: PydanticObjectId,
    user: User = Depends(current_active_user),
) -> Response:
    """
    delete by id
    """
    # annotating
    await Entry.find_one({"_id": entry_id, "owner_id": user.id}).delete()
    return resp.result(state.Ok, data={})


@router.get("/user-entries/search/", response_model=list[Entry])
async def search_user_entries(
    q: str = Query(default=None, max_length=50, description="fuzzy:name、description"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
    user: User = Depends(current_active_user),
) -> Response:
    """
    get by fuzzy query then paged
    """
    # annotating
    filters = {}
    if q:
        filters = {
            "$or": [{"title": {"$regex": q}}, {"summary": {"$regex": q}}],
            "owner_id": user.id,
        }

    db_data = await paginated_find(Entry, filters, current, page_size, sort)

    return resp.result(state.Ok, data=db_data)


@router.post("/user-entry/query/", response_model=list[Entry])
async def query_user_entries(
    filters: dict = Body(default=None, example={"name": "string"}, description="query"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
    user: User = Depends(current_active_user),
) -> Response:
    """
    post filters for query then paged
    """
    # annotating
    filters = {**filters, "owner_id": user.id}
    db_data = await paginated_find(Entry, filters, current, page_size, sort)
    return resp.result(state.Ok, data=db_data)
