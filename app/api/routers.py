from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.api_v1.api import api_router
from app.api.api_v1.endpoints import auth
from app.config import settings


def register_router(app: FastAPI):
    # Include routers for API endpoints.
    app.include_router(api_router, prefix=settings.api_prefix)
    app.include_router(auth.router, prefix="/auth", tags=["auth"])

    # Define a root endpoint that returns a JSON response with a message.
    @app.get("/")
    async def root() -> JSONResponse:
        return JSONResponse(content={"message": "Hello World"})
