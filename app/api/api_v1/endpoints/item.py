import json
from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Query
from pydantic import Json

from app.crud.users import current_active_user
from app.items_example import crud, model, schema
from app.models.users import User
from app.utils.response_model import ResponseModel
from app.utils.tools_func import paginated_find

router = APIRouter()


@router.post("/item", response_model=ResponseModel)
async def create_item(item: schema.ItemCreate):
    """
    create a new
    """
    # annotating
    db_data = await crud.create_item(item)
    return ResponseModel(success=True, data=db_data)


@router.get("/items", response_model=ResponseModel)
async def list_items(
    _id: PydanticObjectId = Query(default=None),
    name: str = Query(default=None, max_length=50, description="fuzzy"),
    description: str = Query(default=None, max_length=50, description="fuzzy"),
    range_create_time: Json = Query(default=None, description=""),
    page_size: int = Query(default=10, description=""),
    current: int = Query(default=1, description=""),
    sort: str = Query(
        default="_id", description="default desc, _id = create_item desc"
    ),
):
    """
    get list by filters then paged
    """
    # annotating
    # range_create_time = json.loads(range_create_time)
    start = datetime.fromisoformat(range_create_time["start"])
    end = datetime.fromisoformat(range_create_time["end"])
    filters = {}
    if _id:
        filters["_id"] = _id
    if name:
        filters["name"] = {"$regex": name}
    if description:
        filters["description"] = {"$regex": description}
    if range_create_time:
        filters["range_create_time"] = {
            "$gte": start,
            "$lte": end,
        }
    db_data = await paginated_find(model.Item, filters, current, page_size, sort)

    return ResponseModel(success=True, data=db_data)


@router.get("/item/{item_id}/", response_model=ResponseModel)
async def get_item(item_id: PydanticObjectId):
    """
    get by id
    """
    # annotating
    db_data = await crud.get_item(item_id)
    return ResponseModel(success=True, data=db_data)


@router.put("/item/{item_id}/", response_model=ResponseModel)
async def update_item(item_id: PydanticObjectId, item: schema.ItemUpdate):
    """
    put by id
    """
    # annotating
    db_data = await crud.update_item(item_id, item)
    return ResponseModel(success=True, data=db_data)


@router.delete("/item/{item_id}/", response_model=ResponseModel)
async def delete_item(item_id: PydanticObjectId):
    """
    delete by id
    """
    # annotating
    await crud.delete_item(item_id)
    return ResponseModel(success=True, data={})


@router.get("/items/search/", response_model=ResponseModel)
async def search_items(
    q: str = Query(max_length=50, default=None, description="fuzzy:name、description"),
    page_size: int = Query(default=10, description=""),
    current: int = Query(default=1, description=""),
    sort: str = Query(
        default="_id", description="default desc, _id = create_item desc"
    ),
):
    """
    get by fuzzy query then paged
    """
    # annotating
    filters = {}
    if q:
        filters = {"$or": [{"name": {"$regex": q}}, {"description": {"$regex": q}}]}

    db_data = await paginated_find(model.Item, filters, current, page_size, sort)

    return ResponseModel(success=True, data=db_data)


@router.post("/item/query/", response_model=ResponseModel)
async def query_items(
    filters: dict = Body(example={"query key": "query value"}, description="query"),
    page_size: int = Query(default=10, description=""),
    current: int = Query(default=1, description=""),
    sort: str = Query(
        default="_id", description="default desc, _id = create_item desc"
    ),
):
    """
    post filters for query then paged
    """
    # annotating
    db_data = await paginated_find(model.Item, filters, current, page_size, sort)
    return ResponseModel(success=True, data=db_data)


@router.post("/user_item", response_model=ResponseModel)
async def create_user_item(
    item: schema.ItemCreate, user: User = Depends(current_active_user)
):
    """
    create a new
    """
    # annotating
    db_data = await crud.create_user_item(item, user.id)
    return ResponseModel(success=True, data=db_data)


@router.get("/user_items/", response_model=ResponseModel)
async def list_user_items(
    q: Annotated[str | None, Query(max_length=50)] = None,
    page_size: int = 10,
    current: int = 1,
    sort: str = "_id",
    user: User = Depends(current_active_user),
):
    """
    get by fuzzy query then paged
    """
    # annotating
    filters = {}
    if q:
        filters = {
            "$or": [{"name": {"$regex": q}}, {"description": {"$regex": q}}],
            "create_by": user.id,
        }
    else:
        filters = {"create_by": user.id}

    db_data = await paginated_find(model.Item, filters, current, page_size, sort)

    return ResponseModel(success=True, data=db_data)


@router.post("/user_item/search/", response_model=ResponseModel)
async def search_user_items(
    filters: dict = Body(example={"query key": "query value"}, title="query"),
    page_size: int = 10,
    current: int = 1,
    sort: str = "_id",
    user: User = Depends(current_active_user),
):
    """
    post filters for search then paged
    """
    # annotating
    filters = {**filters, "create_by": user.id}
    db_data = await paginated_find(model.Item, filters, current, page_size, sort)
    return ResponseModel(success=True, data=db_data)


@router.get("/user_item/{item_id}/", response_model=ResponseModel)
async def get_user_item(
    item_id: PydanticObjectId, user: User = Depends(current_active_user)
):
    """
    get by id and current_user
    """
    # annotating
    db_data = await crud.get_user_item(item_id, user.id)
    return ResponseModel(success=True, data=db_data)


@router.put("/user_item/{item_id}/", response_model=ResponseModel)
async def update_user_item(
    item_id: PydanticObjectId,
    item: schema.ItemUpdate,
    user: User = Depends(current_active_user),
):
    """
    put by id
    """
    # annotating
    db_data = await crud.update_user_item(item_id, item, user.id)
    return ResponseModel(success=True, data=db_data)


@router.delete("/user_item/{item_id}/", response_model=ResponseModel)
async def delete_user_item(
    item_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
    delete by id
    """
    # annotating
    await crud.delete_user_item(item_id, user.id)
    return ResponseModel(success=True, data={})
