from app.models.mans import Man
from app.schemas.mans import ManCreate, ManUpdate

from typing import List
from fastapi import HTTPException


async def create_man(man: ManCreate) -> Man:
    db_man = Man(**man.dict())
    await db_man.create()
    return db_man


async def get_mans() -> List[Man]:
    mans = await Man.all().to_list()
    return mans


async def get_man(man_id: str) -> Man:
    db_man = await Man.find_one(man_id)
    if not db_man:
        raise HTTPException(status_code=404, detail="Man not found")
    return db_man


async def update_user(man_id: str, man: ManUpdate) -> Man:
    db_man = await get_man(man_id)
    await db_man.update_from_dict(man.dict(exclude_unset=True)).save()
    return db_man


async def delete_user(man_id: str) -> None:
    db_man = await get_man(man_id)
    await db_man.delete()
