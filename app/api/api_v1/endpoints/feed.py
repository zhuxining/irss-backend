from datetime import datetime

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import Response
from pydantic import HttpUrl, Json

from app.common.response import resp, state
from app.core.feed_parser import parse_feed
from app.core.users import current_active_user
from app.models.feeds import Feed
from app.models.users import User
from app.schemas.feeds import FeedBase, FeedCreate, FeedUpdate
from app.utils.tools_func import paginated_find
from app.crud.feeds import c_feed, r_feed

router = APIRouter()


@router.get("/parser/")
async def parser_url(url: HttpUrl) -> Response:
    feed, entries = await parse_feed(url)
    return resp.result(state.Ok, data=entries)


@router.get("/parser0/")
async def parser_url_feed(url: HttpUrl) -> Response:
    feed, entries = await parse_feed(url)
    return resp.result(state.Ok, data=feed)


@router.get("/parser1/")
async def parser_url_entry(url: HttpUrl) -> Response:
    feed, entries = await parse_feed(url)
    return resp.result(state.Ok, data=entries)


@router.get("/parser2/")
async def create(url: HttpUrl, display_title: str) -> Response:
    feed, entries = await parse_feed(url)
    db_feed = FeedCreate(**feed.dict())
    db_feed.display_title = display_title
    db_data = await c_feed(db_feed)
    return resp.result(state.Ok, data=db_data)


@router.post("/", response_model=Feed)
async def create_feed(feed: FeedCreate) -> Response:
    """
    Create a new feed.
    """
    db_data = await c_feed(feed)
    return resp.result(state.Ok, data=db_data)


@router.get("/", response_model=list[Feed], response_description="list of feeds")
async def list_feeds(
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
    Get a list of feeds by filters and pagination.
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
    db_data = await paginated_find(Feed, filters, current, page_size, sort)

    return resp.result(state.Ok, data=db_data)


@router.get("/{feed_id}/", response_model=Feed)
async def get_feed(feed_id: PydanticObjectId) -> Response:
    """
    Get an feed by ID.
    """
    db_data = await Feed.find_one({"_id": feed_id})

    # Return a 404 error if the feed is not found.
    if db_data is None:
        return resp.result(state.DataNotFound)
    return resp.result(state.Ok, data=db_data)


@router.put("/{feed_id}/", response_model=Feed)
async def update_feed(feed_id: PydanticObjectId, feed: FeedUpdate) -> Response:
    """
    Update an feed by ID.
    """
    # Set the update_time field to the current time before updating in the database.
    db_data = await Feed.find_one({"_id": feed_id}).update_one(
        {"$set": {**feed.dict(), "update_time": datetime.utcnow()}}
    )
    db_result = await Feed.find_one({"_id": feed_id})
    return resp.result(state.Ok, data=db_result)


@router.delete("/{feed_id}/", response_model={})
async def delete_feed(feed_id: PydanticObjectId) -> Response:
    """
    delete by id
    """
    # annotating
    await Feed.find_one({"_id": feed_id}).delete()
    return resp.result(state.Ok, data={})


@router.post("/query/", response_model=list[Feed])
async def query_feeds(
    filters: dict = Body(default=None, example={"name": "string"}, description="query"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        desctiription="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
) -> Response:
    """
    post filters for query then paged
    """
    # annotating
    db_data = await paginated_find(Feed, filters, current, page_size, sort)
    return resp.result(state.Ok, data=db_data)


@router.post("/user-feed", response_model=Feed)
async def create_user_feed(
    feed: FeedCreate, user: User = Depends(current_active_user)
) -> Response:
    """
    create a new
    """
    # annotating
    db_feed = Feed(**feed.dict())
    db_feed.owner_id = user.id
    db_feed.create_time = datetime.utcnow()
    db_data = await Feed.insert_one(db_feed)
    return resp.result(state.Ok, data=db_data)


@router.get("/user-feeds/", response_model=Feed)
async def list_user_feeds(
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
    db_data = await paginated_find(Feed, filters, current, page_size, sort)
    return resp.result(state.Ok, data=db_data)


@router.get("/user-feed/{feed_id}/", response_model=Feed)
async def get_user_feed(
    feed_id: PydanticObjectId, user: User = Depends(current_active_user)
) -> Response:
    """
    get by id and current_user
    """
    # annotating
    db_data = await Feed.find_one({"owner_id": user.id, "_id": feed_id})
    return resp.result(state.Ok, data=db_data)


@router.put("/user-feed/{feed_id}/", response_model=Feed)
async def update_user_feed(
    feed_id: PydanticObjectId,
    feed: FeedUpdate,
    user: User = Depends(current_active_user),
) -> Response:
    """
    put by id
    """
    # annotating
    db_data = await Feed.find_one({"_id": feed_id}).update_one(
        {
            "$set": {
                **feed.dict(),
                "update_by": user.id,
                "update_time": datetime.utcnow(),
            }
        }
    )
    db_result = await Feed.find_one({"_id": feed_id})
    return resp.result(state.Ok, data=db_result)


@router.delete("/user-feed/{feed_id}/", response_model={})
async def delete_user_feed(
    feed_id: PydanticObjectId,
    user: User = Depends(current_active_user),
) -> Response:
    """
    delete by id
    """
    # annotating
    await Feed.find_one({"_id": feed_id, "owner_id": user.id}).delete()
    return resp.result(state.Ok, data={})


@router.get("/user-feeds/search/", response_model=list[Feed])
async def search_user_feeds(
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
            "$or": [{"title": {"$regex": q}}, {"subtitle": {"$regex": q}}],
            "owner_id": user.id,
        }

    db_data = await paginated_find(Feed, filters, current, page_size, sort)

    return resp.result(state.Ok, data=db_data)


@router.post("/user-feed/query/", response_model=list[Feed])
async def query_user_feeds(
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
    db_data = await paginated_find(Feed, filters, current, page_size, sort)
    return resp.result(state.Ok, data=db_data)
