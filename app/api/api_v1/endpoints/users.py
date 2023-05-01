from fastapi import APIRouter

from app.schemas.users import UserRead, UserUpdate
from app.crud.users import fastapi_users

router = APIRouter()


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)
