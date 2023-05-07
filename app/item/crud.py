from bson import ObjectId
from app.item import model, schema
from app.item.model import Item

from typing import List
from fastapi import HTTPException


async def create_item(item: schema.ItemCreate) -> Item:
    db_item = Item(**item.dict())
    await Item.save(db_item)
    return db_item


async def get_items() -> List[Item]:
    db_items = await Item.find_all().limit(3).to_list()
    return db_items


async def get_item(item_id: str) -> Item:
    db_item = await Item.find_one({"_id": ObjectId(item_id)})
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


async def update_item(item_id: str, item: schema.ItemUpdate) -> Item:
    db_item = await Item.find_one({"_id": ObjectId(item_id)})
    db_item = Item(**item.dict())
    await Item.update(db_item)
    return db_item


async def delete_item(item_id: str):
    db_item = await Item.find_one({"_id": ObjectId(item_id)})
    await db_item.delete()
