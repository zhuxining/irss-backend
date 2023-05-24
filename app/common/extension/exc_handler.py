import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError

from app.common.logger import log
from app.common.response import resp, state


# Define Frame exception handlers for RequestValidationError and PyMongoError.
def register_exception(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        log.warning(f"\nErrorDetail:{exc.errors()}\n{traceback.format_exc()}")
        return resp.result(state.ValidationError, error_detail=exc.errors())

    @app.exception_handler(PyMongoError)
    async def pymongo_error_handle(request: Request, exc: PyMongoError):
        log.warning(f"\nErrorDetail:{exc}\n{traceback.format_exc()}")
        return resp.result(state.SqlFail, error_detail=exc)

    # Define user-defined exception handlers for RespError, and set an error_detail.
    @app.exception_handler(state.State)
    async def logic_error_handle(request: Request, exc: state.State):
        log.debug(f"\nErrorDetail:{exc}\n{traceback.format_exc()}")
        return resp.result(
            # state=exc, error_detail="Business Logic Error, Not Frame Error"
            state=exc,
            error_detail=traceback.format_exc(),
        )
