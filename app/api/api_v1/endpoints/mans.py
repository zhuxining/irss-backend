from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from typing import List
from app.models.mans import Man
from app.schemas.mans import ManCreate, ManUpdate
from app.crud.mans import create_man, get_man, get_mans, update_user, delete_user

router = APIRouter()


@router.post("/mans", response_model=Man)
async def create_man(man: ManCreate):
    return await create_man(man)


@router.get("/mans", response_model=List[Man])
async def get_mans():
    return await get_mans()


@router.get("/mans/{man_id}", response_model=Man)
async def get_man(man_id: str):
    return await get_man(man_id)


@router.put("/mans/{man_id}", response_model=Man)
async def update_man(man_id: str, man: ManUpdate):
    return await update_man(man_id, man)


@router.delete("/mans/{man_id}")
async def delete_man(man_id: str):
    await delete_man(man_id)
    return {"message": "Man deleted successfully"}
