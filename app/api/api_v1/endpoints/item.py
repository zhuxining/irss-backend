from typing import Annotated, List, Optional

from bson import ObjectId
from fastapi import APIRouter, Body, Path, Query

from app.items_example import crud, model, schema
from app.utils.paged import paginated_find
from app.utils.response_model import ResponseModel

router = APIRouter()


@router.post("/item", response_model=ResponseModel)
async def create_item(item: schema.ItemCreate):
    """
    # 请求体
    """
    #
    db_data = await crud.create_item(item)
    return ResponseModel(success=True, data=db_data)


@router.get("/item/", response_model=ResponseModel)
async def get_items(
    q: Annotated[str | None, Query(max_length=50)] = None,
    page_size: int = 10,
    current: int = 1,
    sort: str = "_id",
):
    """
    # 请求体
    """
    #
    filters = {}
    if q:
        filters["$or"] = [{"name": {"$regex": q}}, {"description": {"$regex": q}}]

    db_data = await paginated_find(model.Item, filters, current, page_size, sort)

    return ResponseModel(success=True, data=db_data)


@router.post("/item/search/", response_model=ResponseModel)
async def search_items(
    filters: dict = Body(example={"key1": "value", "key2": "value"}),
    page_size: int = 10,
    current: int = 1,
    sort: str = "_id",
):
    """
    # 请求体
    """
    #
    db_data = await paginated_find(model.Item, filters, current, page_size, sort)
    return ResponseModel(success=True, data=db_data)


@router.get("/item/{item_id}/", response_model=ResponseModel)
async def get_item(item_id: str):
    """
    # 请求体
    """
    #
    db_data = await crud.get_item(item_id)
    return ResponseModel(success=True, data=db_data)


@router.put("/{item_id}/", response_model=ResponseModel)
async def update_item(item_id: str, item: schema.ItemUpdate):
    """
    # 请求体
    """
    #
    db_data = await crud.update_item(item_id, item)
    return ResponseModel(success=True, data=db_data)


@router.delete("/item/{item_id}/", response_model=ResponseModel)
async def delete_item(item_id: str):
    """
    # 请求体
    """
    #
    await crud.delete_item(item_id)
    return ResponseModel(success=True, data={})
