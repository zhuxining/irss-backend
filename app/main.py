import time
import traceback

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pymongo.errors import PyMongoError

from app.api.api_v1.api import api_router
from app.api.api_v1.endpoints import auth
from app.config import settings
from app.db.init_db import init_db
from app.utils import resp


# from app.extensions.exc_handler import log_requests

app = FastAPI(
    debug=False,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    openapi_url=f"{settings.api_prefix}/openapi.json",
)

# Include routers for API endpoints.
app.include_router(api_router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Add middleware to the application.

# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(
#     TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
# )
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define exception handlers for RequestValidationError and PyMongoError.
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.warning(
        f"\nMethod:{request.method} URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
    )
    # Return a JSON response with error details.
    return resp.result(resp.ValidationError, error_detail=exc.errors())


@app.exception_handler(PyMongoError)
async def handle_pymongo_error(request, exc):
    logger.warning(
        f"\nMethod:{request.method} URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
    )

    return resp.result(resp.SqlFail, error_detail=exc)


# Define a middleware function to log incoming requests and outgoing responses.
@app.middleware("http")
async def log_requests(request: Request, call_next) -> str:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        f"\nMethod:{request.method}\nURL:{request.url}\nHeaders:{request.headers}\nProcessTime:{process_time}\n{traceback.format_exc()}"
    )

    return response


# Define a root endpoint that returns a JSON response with a message.
@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"message": "Hello World"})


# Define an event handler for application startup that initializes the database connection.
@app.on_event("startup")
async def on_startup() -> None:
    print("---startup---")
    await init_db()
    logger.info("Application startup")


# Define an event handler for application shutdown that logs a message.
@app.on_event("shutdown")
def shutdown_event() -> None:
    print("---shutdown---")
    logger.info("Application shutdown")
