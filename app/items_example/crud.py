from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException

from app.items_example import model, schema


async def create_item(item: schema.ItemCreate) -> model.Item:
    db_item = model.Item(**item.dict())
    db_item.created_at = datetime.utcnow()
    await model.Item.insert_one(db_item)
    return db_item


async def get_items() -> list[model.Item]:
    db_items = await model.Item.find_all().to_list()
    return db_items


async def get_item(item_id: PydanticObjectId) -> model.Item:
    db_item = await model.Item.find_one({"_id": item_id})
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


async def update_item(
    item_id: PydanticObjectId,
    item: schema.ItemUpdate,
) -> model.Item:
    await model.Item.find_one({"_id": item_id}).update_one(
        {"$set": {**item.dict(), "updated_at": datetime.utcnow()}}
    )
    return await get_item(item_id)


async def delete_item(item_id: PydanticObjectId):
    await model.Item.find_one({"_id": item_id}).delete()


async def create_user_item(
    item: schema.ItemCreate, created_by: PydanticObjectId | None
) -> model.Item:
    db_item = model.Item(**item.dict())
    db_item.created_by = created_by
    db_item.created_at = datetime.utcnow()
    await model.Item.insert_one(db_item)
    return db_item


async def get_user_items(user_id: PydanticObjectId | None) -> list[model.Item]:
    db_items = await model.Item.find({"created_by": user_id}).to_list()
    return db_items


async def get_user_item(
    item_id: PydanticObjectId, user_id: PydanticObjectId | None
) -> model.Item:
    db_item = await model.Item.find_one({"created_by": user_id, "_id": item_id})
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


async def update_user_item(
    item_id: PydanticObjectId,
    item: schema.ItemUpdate,
    updated_by: PydanticObjectId | None,
) -> model.Item:
    await model.Item.find_one({"_id": item_id}).update_one(
        {
            "$set": {
                **item.dict(),
                "updated_by": updated_by,
                "updated_at": datetime.utcnow(),
            }
        }
    )
    return await get_item(item_id)


async def delete_user_item(item_id: PydanticObjectId, user_id: PydanticObjectId | None):
    await model.Item.find_one({"_id": item_id, "created_by": user_id}).delete()
