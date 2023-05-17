import traceback

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

from app.extensions.logger import logger
from app.utils.response_model import ResponseModel

from .api.api_v1.api import api_router
from .api.api_v1.endpoints import auth
from .config import settings
from .db.init_db import init_db

app = FastAPI(
    debug=False,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    openapi_url=f"{settings.api_prefix}/openapi.json",
)


# async def handle_pymongo_error(request, exc):
#     logger.exception(str(exc))
#     response = {"detail": "Internal Server Error", "log_id": 123}  # Example log ID
#     return JSONResponse(response, status_code=500)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#     )


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
