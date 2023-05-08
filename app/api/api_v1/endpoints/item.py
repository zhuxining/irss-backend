from datetime import date
from sre_constants import SUCCESS
from bson import ObjectId
from fastapi import APIRouter, Path, Query

from typing import List, Annotated

from app.items_example import schema, crud, model
from app.items_example.model import Item
from fastapi import HTTPException, status

from app.utils.paged import paginated_find
from app.utils.response_format import ResponseModel


router = APIRouter()


@router.post("/item", response_model=ResponseModel)
async def create_item(item: schema.ItemCreate):
    db_data = await crud.create_item(item)
    return ResponseModel(success=True, data=db_data)


# @router.get("/items", response_model=List[schema.Item])
# async def get_items():
#     return await crud.get_items()


@router.get("/items", response_model=ResponseModel)
async def get_items(
    q: Annotated[list[str] | None, Query()] = ["name", "description"],
    page_size: int = 10,
    current: int = 1,
    sort: str = "_id",
):
    query_items = {"q": q}
    db_data = await paginated_find(Item, {}, current, page_size, sort)

    return ResponseModel(success=True, data=db_data)


@router.get("/items/{item_id}", response_model=ResponseModel)
async def get_item(item_id: str):
    db_data = await crud.get_item(item_id)
    return ResponseModel(success=True, data=db_data)


@router.put("/items/{item_id}", response_model=ResponseModel)
async def update_item(item_id: str, item: schema.ItemUpdate):
    db_data = await crud.update_item(item_id, item)
    return ResponseModel(success=True, data=db_data)


@router.delete("/items/{item_id}", response_model=ResponseModel)
async def delete_item(item_id: str):
    await crud.delete_item(item_id)
    return ResponseModel(success=True, data={})
