from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, entry, feed, item, user

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(item.router, prefix="/example", tags=["example"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(feed.router, prefix="/feed", tags=["feed"])
api_router.include_router(entry.router, prefix="/entry", tags=["entry"])
