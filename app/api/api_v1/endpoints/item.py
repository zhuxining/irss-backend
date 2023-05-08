from datetime import date
from bson import ObjectId
from fastapi import APIRouter, Path

from typing import List

from app.items_example import schema, crud, model
from app.items_example.model import Item
from fastapi import HTTPException

from app.utils.paged import paginated_find
from app.utils.response_format import ResponseModel

router = APIRouter()


@router.post("/item", response_model=schema.Item)
async def create_item(item: schema.ItemCreate):
    return await crud.create_item(item)


# @router.get("/items", response_model=List[schema.Item])
# async def get_items():
#     return await crud.get_items()


@router.get("/items")
async def get_items(page_size: int = 10, current: int = 1, sort: str = "_id"):
    # await paginated_find(model.Item, {}, page_size, page, sort)
    db_date = await paginated_find(Item, {}, current, page_size, sort)
    return ResponseModel(success=True, data=db_date)


@router.get("/items/{item_id}", response_model=schema.Item)
async def get_item(item_id: str):
    return await crud.get_item(item_id)


@router.put("/items/{item_id}", response_model=schema.Item)
async def update_item(item_id: str, item: schema.ItemUpdate):
    return await crud.update_item(item_id, item)


@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    await crud.delete_item(item_id)
    return {"message": "Item deleted successfully"}
