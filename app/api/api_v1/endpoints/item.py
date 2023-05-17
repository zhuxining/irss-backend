from datetime import date, datetime

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Query
from pydantic import Json

# from app.api.resp import Resp, fail
from app.api import resp
from app.crud.users import current_active_user
from app.items_example import crud, model, schema
from app.models.users import User
from app.utils.response_model import ResponseModel
from app.utils.tools_func import paginated_find

router = APIRouter()


@router.get("/table/list", response_model=list[schema.ItemBase])
async def get_table_list():
    return resp.result(resp.OK)


@router.get("/table/list-fail")
async def get_table_list_fail():
    return resp.result(resp.InvalidParams)


@router.post("/item", response_model=schema.Item)
async def create_item(item: schema.ItemCreate):
    """
    create a new
    """
    # annotating
    db_data = await crud.create_item(item)
    return resp.result(resp.OK, data=db_data)


@router.get("/items", response_model=ResponseModel)
async def list_items(
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
    range_num: Json = Query(
        default=None,
        example={"min_value": 0, "max_value": 100},
        description="json",
    ),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
):
    """
    get list by filters then paged
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
    if range_num:
        filters["num"] = {
            "$gte": range_num["min_value"],
            "$lte": range_num["max_value"],
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
    q: str = Query(default=None, max_length=50, description="fuzzy:name、description"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
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
    filters: dict = Body(default=None, example={"name": "string"}, description="query"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
):
    """
    post filters for query then paged
    """
    # annotating
    db_data = await paginated_find(model.Item, filters, current, page_size, sort)
    return ResponseModel(success=True, data=db_data)


@router.post("/user-item", response_model=ResponseModel)
async def create_user_item(
    item: schema.ItemCreate, user: User = Depends(current_active_user)
):
    """
    create a new
    """
    # annotating
    db_data = await crud.create_user_item(item, user.id)
    return ResponseModel(success=True, data=db_data)


@router.get("/user-items/", response_model=ResponseModel)
async def list_user_items(
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
    range_num: Json = Query(
        default=None,
        example={"min_value": 0, "max_value": 100},
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
):
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
    if range_num:
        filters["num"] = {
            "$gte": range_num["min_value"],
            "$lte": range_num["max_value"],
        }
    filters = {**filters, "create_by": user.id}
    db_data = await paginated_find(model.Item, filters, current, page_size, sort)
    return ResponseModel(success=True, data=db_data)


@router.get("/user-item/{item_id}/", response_model=ResponseModel)
async def get_user_item(
    item_id: PydanticObjectId, user: User = Depends(current_active_user)
):
    """
    get by id and current_user
    """
    # annotating
    db_data = await crud.get_user_item(item_id, user.id)
    return ResponseModel(success=True, data=db_data)


@router.put("/user-item/{item_id}/", response_model=ResponseModel)
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


@router.delete("/user-item/{item_id}/", response_model=ResponseModel)
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


@router.get("/user-items/search/", response_model=ResponseModel)
async def search_user_items(
    q: str = Query(default=None, max_length=50, description="fuzzy:name、description"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
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

    db_data = await paginated_find(model.Item, filters, current, page_size, sort)

    return ResponseModel(success=True, data=db_data)


@router.post("/user-item/query/", response_model=ResponseModel)
async def query_user_items(
    filters: dict = Body(default=None, example={"name": "string"}, description="query"),
    page_size: int = Query(example=10, description=""),
    current: int = Query(example=1, description=""),
    sort: str = Query(
        default="create_time",
        example="'id':-1",
        description="1:asc, -1:desc, default desc, _id = create_time desc",
    ),
    user: User = Depends(current_active_user),
):
    """
    post filters for query then paged
    """
    # annotating
    filters = {**filters, "create_by": user.id}
    db_data = await paginated_find(model.Item, filters, current, page_size, sort)
    return ResponseModel(success=True, data=db_data)