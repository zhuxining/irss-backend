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


# Define an event handler for application startup that initializes the database connection.
@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
    log.success("Application startup")


# Define an event handler for application shutdown that logs a message.
@app.on_event("shutdown")
def shutdown_event() -> None:
    log.success("Application shutdown")
