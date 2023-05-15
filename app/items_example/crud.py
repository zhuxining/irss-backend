from typing import List

from bson import ObjectId
from fastapi import HTTPException

from app.items_example import model, schema
from app.items_example.model import Item


async def create_item(item: schema.ItemCreate) -> model.Item:
    db_item = Item(**item.dict())
    await Item.insert_one(db_item)
    return db_item


async def get_items() -> List[Item]:
    db_items = await Item.find_all().to_list()
    return db_items


async def get_item(item_id: str) -> Item:
    db_item = await Item.find_one({"_id": ObjectId(item_id)})
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


async def update_item(item_id: str, item: schema.ItemUpdate) -> Item:
    await model.Item.find_one({"_id": ObjectId(item_id)}).update_one({"$set": item})
    return await get_item(item_id)


async def delete_item(item_id: str):
    await Item.find_one({"_id": ObjectId(item_id)}).delete()
