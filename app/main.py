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
    """
    请求参数验证异常
    :param request: 请求头信息
    :param exc: 异常对象
    :return:
    """
    # 日志记录异常详细上下文
    logger.error(
        f"全局异\n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
    )
    return resp.result(resp.InvalidParams, data=exc.errors())


app.include_router(api_router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    print("---startup---")
    await init_db()
    # app.add_exception_handler(PyMongoError, handle_pymongo_error)


@app.on_event("shutdown")
def shutdown_event():
    print("---shutdown---")
