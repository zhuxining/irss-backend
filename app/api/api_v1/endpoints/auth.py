from fastapi import APIRouter, Depends

from app.core.users import (
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)
from app.models.users import User
from app.schemas.users import UserCreate, UserRead
from app.config import settings

router = APIRouter()
SECRET = settings.token_secret_key

router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/jwt")
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/google",
)


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
