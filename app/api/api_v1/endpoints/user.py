from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter

from app.common.response import resp, state
from app.core.users import fastapi_users
from app.models.users import User
from app.schemas.users import UserRead, UserUpdate

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
    db_data = await User.find_one({"_id": user_id}).project(UserRead)
    return resp.result(state.Ok, data=db_data)
