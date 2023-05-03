from fastapi import APIRouter

from app.api.api_v1.endpoints import users, auth, mans, feeds

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(feeds.router, prefix="/feeds", tags=["feeds"])
api_router.include_router(mans.router, prefix="/example")
