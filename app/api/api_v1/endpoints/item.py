from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Query

from app.crud.users import current_active_user
from app.items_example import crud, model, schema
from app.models.users import User
from app.utils.tools_func import paginated_find
from app.utils.response_model import ResponseModel

router = APIRouter()


@router.post("/item", response_model=ResponseModel)
async def create_item(item: schema.ItemCreate):
    """
    create a new
    """
    # annotating
    db_data = await crud.create_item(item)
    return ResponseModel(success=True, data=db_data)


@router.get("/items/", response_model=ResponseModel)
async def list_items(
    q: Annotated[str | None, Query(max_length=50)] = None,
    page_size: int = 10,
    current: int = 1,
    sort: str = "_id",
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


@router.post("/item/search/", response_model=ResponseModel)
async def search_items(
    filters: dict = Body(example={"query key": "query value"}, title="query"),
    page_size: int = 10,
    current: int = 1,
    sort: str = "_id",
):
    """
    post filters for search then paged
    """
    # annotating
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
