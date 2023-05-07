from bson import ObjectId
from fastapi import APIRouter

from typing import List

from app.item import schema, crud, model
from app.item.crud import get_items
from fastapi import HTTPException

router = APIRouter()


@router.post("/item", response_model=schema.Item)
async def create_item(item: schema.ItemCreate):
    return await crud.create_item(item)


# @router.get("/items", response_model=List[schema.Item])
# async def get_items():
#     db_items = await model.Item.all().to_list()
#     return db_items


@router.get("/items", response_model=List[schema.Item])
async def get_items():
    return await crud.get_items()


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
