import motor.motor_asyncio

from app.config import settings

DATABASE_URL = settings.db_url
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["irss-test"]
