from datetime import datetime

from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Body, Depends, Query
from fastapi.responses import Response
from pydantic import HttpUrl, Json

from app.common.response import resp, state
from app.core.entry_append import user_entry_append
from app.core.users import current_active_user
from app.models.entries import Entry
from app.models.users import User
from app.schemas.entries import EntryRead, EntryUpdate
from app.utils.tools_func import paginated_find

router = APIRouter()


@router.get("/", response_model=list[EntryRead], response_description="list of entries")
async def list_entries(
    feed_url: HttpUrl = Query(default=None),
    is_read: bool = Query(default=False),
    read_later: bool = Query(default=False),
    is_hide: bool = Query(default=False),
    is_star: bool = Query(default=False),
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
    if feed_url:
        filters["feed_url"] = {"$regex": feed_url}
    if is_read:
        filters["is_read"] = is_read
    if read_later:
        filters["read_later"] = read_later
    if is_hide:
        filters["is_hide"] = is_hide
    if is_star:
        filters["is_star"] = is_star
    if range_create_time:
        start: datetime = datetime.fromisoformat(range_create_time["start_time"])
        end: datetime = datetime.fromisoformat(range_create_time["end_time"])

        # Use $gt and $lt instead of $gte and $lte to exclude the start and end times.
        filters["create_time"] = {
            "$gte": start,
            "$lte": end,
        }
    db_data = await paginated_find(Entry, filters, current, page_size, sort)

    return resp.result(state.Ok, data=db_data)


@router.get("/search/", response_model=list[EntryRead])
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


@router.get("/user-entries/", response_model=EntryRead)
async def list_user_entries(
    background_tasks: BackgroundTasks,
    is_reload_parser: bool = Query(default=False),
    feed_url: HttpUrl = Query(default=None),
    is_read: bool = Query(default=False),
    read_later: bool = Query(default=False),
    is_hide: bool = Query(default=False),
    is_star: bool = Query(default=False),
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
    Get a list of entries by filters and pagination.
    """
    # Use the correct sorting order for descending order.

    filters = {}
    if feed_url:
        filters["feed_url"] = {"$regex": feed_url}
    if is_read:
        filters["is_read"] = is_read
    if read_later:
        filters["read_later"] = read_later
    if is_hide:
        filters["is_hide"] = is_hide
    if is_star:
        filters["is_star"] = is_star
    if range_create_time:
        start: datetime = datetime.fromisoformat(range_create_time["start_time"])
        end: datetime = datetime.fromisoformat(range_create_time["end_time"])

        # Use $gt and $lt instead of $gte and $lte to exclude the start and end times.
        filters["create_time"] = {
            "$gte": start,
            "$lte": end,
        }

    filters = {**filters, "owner_id": user.id}
    if is_reload_parser:
        await user_entry_append(user.id)
    db_data = await paginated_find(Entry, filters, current, page_size, sort)
    return resp.result(state.Ok, data=db_data)


@router.put("/user-entry/{entry_id}/", response_model=EntryRead)
async def update_entry(
    entry_id: PydanticObjectId,
    entry: EntryUpdate,
    user: User = Depends(current_active_user),
) -> Response:
    """
    Update an entry by ID.
    """
    # Set the update_time field to the current time before updating in the database.
    db_data = await Entry.find_one({"_id": entry_id}, {"owner_id": user.id})
    if db_data is None:
        raise state.NotFound
    read_modified = (
        db_data.read_modified  # type: ignore
        if (entry.is_read == db_data.is_read)  # type: ignore
        else datetime.utcnow()
    )
    read_later_modified = (
        db_data.read_later_modified  # type: ignore
        if (entry.read_later == db_data.read_later)  # type: ignore
        else datetime.utcnow()
    )
    hide_modified = (
        db_data.hide_modified  # type: ignore
        if (entry.is_hide == db_data.is_hide)  # type: ignore
        else datetime.utcnow()
    )
    await Entry.find_one({"_id": entry_id}).update_one(
        {
            "$set": {
                **entry.dict(),
                "read_modified": read_modified,
                "read_later_modified": read_later_modified,
                "hide_modified": hide_modified,
                "update_time": datetime.utcnow(),
            }
        }
    )
    db_result = await Entry.find_one({"_id": entry_id})
    return resp.result(state.Ok, data=db_result)


@router.get("/user-entries/search/", response_model=list[EntryRead])
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


@router.post("/user-entry/query/", response_model=list[EntryRead])
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
