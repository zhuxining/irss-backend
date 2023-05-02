from beanie import init_beanie

from app.models.users import User
from app.models import mans
from app.db.database import db


async def init_db():
    await init_beanie(
        database=db,
        document_models=[
            User,
            mans.Man,
        ],  # type: ignore
    )
