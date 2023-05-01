import select
from shutil import which
from threading import get_ident
from app.models.feeds import Feed
from db.database import async_session_maker
from app import models, schemas


# def get_feeds(skip: int = 0, limit: int = 100):
#     async with async_session_maker() as session:
#         sql = select(Feed).where()
#         feeds = session.execute(sql)

#     return feeds
