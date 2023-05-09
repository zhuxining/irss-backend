from fastapi import FastAPI

from .api.api_v1.api import api_router
from .api.api_v1.endpoints import auth
from .config import settings
from .db.init_db import init_db

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    openapi_url=f"{settings.api_prefix}/openapi.json",
)

app.include_router(api_router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    print("---startup---")
    await init_db()


@app.on_event("shutdown")
def shutdown_event():
    print("---shutdown---")
