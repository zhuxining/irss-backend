# import traceback

# from app.main import app

# from .logger import logger


# @app.middleware("http")
# async def log_requests(request, call_next):
#     logger.info(
#         f"\nMethod:{request.method}\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
#     )
#     response = await call_next(request)
#     return response
