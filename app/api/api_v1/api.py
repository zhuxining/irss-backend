from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, item, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(item.router, prefix="/example", tags=["example"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
