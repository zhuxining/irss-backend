import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError

from app.common.logger import log
from app.common.response import resp


# Define Frame exception handlers for RequestValidationError and PyMongoError.
def register_exception(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        log.warning(
            f"\nMethod:{request.method} URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        )
        return resp.result(resp.ValidationError, error_detail=exc.errors())

    @app.exception_handler(PyMongoError)
    async def pymongo_error_handle(request, exc):
        log.warning(
            f"\nMethod:{request.method} URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        )
        return resp.result(resp.SqlFail, error_detail=exc)

    # Define user-defined exception handlers for RespError.
    @app.exception_handler(resp.Resp)
    async def logic_error_handle(request: Request, exc: resp.Resp):
        return resp.result(
            resp=exc, error_detail="Business Logic Error, Not Frame Error"
        )
