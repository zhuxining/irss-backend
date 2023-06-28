import time
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.common.logger import log
from app.config import settings


# Add middleware to the application.
def register_middleware(app: FastAPI) -> None:
    if settings.middleware_https_redirect:
        app.add_middleware(HTTPSRedirectMiddleware)

    if settings.middleware_trusted_host:
        app.add_middleware(
            TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
        )

    if settings.middleware_gzip:
        app.add_middleware(GZipMiddleware, minimum_size=1000)

    if settings.middleware_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Define a middleware function to log incoming requests and outgoing responses.
    @app.middleware("http")
    async def log_requests(request: Request, call_next) -> str:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        if 500 > response.status_code >= 400:
            log.warning(
                f"\nMethod:{request.method} \nURL:{request.url}\nHeaders:{request.headers}\nClient:{request.client}\nCookies:{request.cookies}\nProcessTime:{process_time}\n{traceback.format_exc()}"
            )
        if 600 > response.status_code >= 500:
            log.error(
                f"\nMethod:{request.method} \nURL:{request.url}\nHeaders:{request.headers}\nClient:{request.client}\nCookies:{request.cookies}\nProcessTime:{process_time}\n{traceback.format_exc()}"
            )
        return response
