from datetime import datetime

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import Response
from pydantic import HttpUrl

from app.common.response import resp, state
from app.core.feed_parser import parse_feed
from app.core.users import current_active_user
from app.crud.feeds import c_feed, r_feed, r_user_feed, r_user_feeds
from app.models.feeds import Feed
from app.models.users import User
from app.schemas.feeds import FeedCreate, FeedParser, FeedRead, FeedUpdate
from app.utils.tools_func import paginated_find

router = APIRouter()


@router.get("/parser", response_model=FeedParser)
async def parser_url(url: HttpUrl) -> Response:
    """
    parser an URL, example:

    https://www.ithome.com/rss/

    https://36kr.com/feed-article
    """
    feed, entries = await parse_feed(url)
    return resp.result(state.Ok, data=feed)


@router.get(
    "/list/", response_model=list[FeedRead], response_description="list of feeds"
)
async def list_feeds(
    id: str = Query(default=None, description="mongodb ObjectId"),
    display_title: str = Query(default=None, max_length=50, description="fuzzy"),
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
    if display_title:
        filters["display_title"] = {"$regex": display_title}
    db_data = await paginated_find(Feed, filters, current, page_size, sort)

    return resp.result(state.Ok, data=db_data)


@router.post("/user-feed/", response_model=FeedRead)
async def create_feed(
    feed_create: FeedCreate, user: User = Depends(current_active_user)
) -> Response:
    """
    Create a new feed.
    """
    feed, entries = await parse_feed(feed_create.url)

    db_data = await Feed.find_one({"owner_id": user.id, "url": feed.url})
    if db_data:
        raise state.AlreadyExists.set_msg("请勿重复添加")
    else:
        data_feed = Feed(**feed.dict())
        if feed_create.display_title:
            data_feed.display_title = feed_create.display_title
        else:
            data_feed.display_title = feed.title
        data_feed.owner_id = user.id
        db_data = await Feed.insert_one(data_feed)
    return resp.result(state.Ok, data=db_data)


@router.get(
    "/user-feed/list",
    response_model=list[FeedRead],
    response_description="list of feeds",
)
async def user_feed_list(
    id: str = Query(default=None, description="mongodb ObjectId"),
    display_title: str = Query(default=None, max_length=50, description="fuzzy"),
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
    Get a list of feeds by filters and pagination.
    """
    # Use the correct sorting order for descending order.

    filters = {}
    if id:
        filters["_id"] = PydanticObjectId(id)
    if display_title:
        filters["display_title"] = {"$regex": display_title}
    db_data = await paginated_find(Feed, filters, current, page_size, sort)
    filters = {**filters, "create_by": user.id}
    return resp.result(state.Ok, data=db_data)


@router.get("/user-feed/{feed_id}/", response_model=FeedRead)
async def get_user_feed(
    feed_id: PydanticObjectId, user: User = Depends(current_active_user)
) -> Response:
    """
    get by id and current_user
    """
    # annotating
    db_data = await Feed.find_one({"owner_id": user.id, "_id": feed_id})
    return resp.result(state.Ok, data=db_data)


@router.put("/user-feed/{feed_id}/", response_model=FeedRead)
async def update_user_feed(
    feed_id: PydanticObjectId,
    feed: FeedUpdate,
    user: User = Depends(current_active_user),
) -> Response:
    """
    put by id
    """
    # annotating
    await Feed.find_one({"_id": feed_id}).update_one(
        {
            "$set": {
                **feed.dict(),
                "update_by": user.id,
                "update_time": datetime.utcnow(),
            }
        }
    )
    db_data = await Feed.find_one({"_id": feed_id})
    return resp.result(state.Ok, data=db_data)


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


@router.get("/user-feed/search/", response_model=list[FeedRead])
async def search_user_feeds(
    q: str = Query(
        default=None, max_length=50, description="fuzzy:display_title、title"
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
    get by fuzzy query then paged
    """
    # annotating
    filters = {}
    if q:
        filters = {
            "$or": [{"display_title": {"$regex": q}}, {"title": {"$regex": q}}],
            "owner_id": user.id,
        }

    db_data = await paginated_find(Feed, filters, current, page_size, sort)

    return resp.result(state.Ok, data=db_data)


@router.post("/user-feed/query/", response_model=list[FeedRead])
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
