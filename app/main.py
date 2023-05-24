from fastapi import FastAPI

from app.api.routers import register_router
from app.common.db.init_db import init_db
from app.common.extension.exc_handler import register_exception
from app.common.logger import log
from app.common.middleware.middleware_add import register_middleware
from app.config import settings

app = FastAPI(
    debug=False,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    openapi_url=f"{settings.api_prefix}/openapi.json",
)

register_router(app)
register_middleware(app)
register_exception(app)


@app.on_event("startup")
async def on_startup() -> None:
    log.success("Application startup")
    await init_db()


@app.on_event("shutdown")
def shutdown_event() -> None:
    log.success("Application shutdown")
