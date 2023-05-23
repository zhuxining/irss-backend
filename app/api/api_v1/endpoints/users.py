from curses.ascii import US
from typing import Any
from fastapi import APIRouter, Response

from app.core.users import fastapi_users
from app.schemas.users import UserRead, UserUpdate
from app.models.users import User
from beanie import PydanticObjectId
from app.common.response import resp

router = APIRouter()


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)


@router.get(
    "/users-find/{user_id}/",
    response_model=UserRead,
    response_model_exclude_unset=True,
    response_model_exclude={"email"},
)
async def get_user(user_id: PydanticObjectId) -> Any:
    UserRead = await User.find_one({"_id": user_id})
    # return resp.result(resp.Ok, data=UserRead)
    return UserRead
