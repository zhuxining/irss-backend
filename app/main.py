import traceback

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

from .api.api_v1.api import api_router
from .api.api_v1.endpoints import auth
from .config import settings
from .db.init_db import init_db
from .extensions.logger import logger

# from .extensions.exc_handler import log_requests
from .utils import resp

app = FastAPI(
    debug=True,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    openapi_url=f"{settings.api_prefix}/openapi.json",
)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.warning(
        f"\nMethod:{request.method} URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
    )
    # （Pydantic's ValidationError） RequestValidationError
    return resp.result(resp.ValidationError, error_detail=exc.errors())


@app.exception_handler(PyMongoError)
async def handle_pymongo_error(request, exc):
    logger.warning(
        f"\nMethod:{request.method} URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
    )
    # PyMongoError
    return resp.result(resp.SqlFail, error_detail=exc)


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(
        f"\nMethod:{request.method}\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
    )
    response = await call_next(request)
    return response


app.include_router(api_router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    print("---startup---")
    await init_db()
    logger.info("Application startup")


@app.on_event("shutdown")
def shutdown_event():
    print("---shutdown---")
    logger.info("Application shutdown")
