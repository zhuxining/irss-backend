from app.db.database import get_async_session


# def get_db():
#     db = get_async_session()
#     yield db


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
