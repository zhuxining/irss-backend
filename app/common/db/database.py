from motor.motor_asyncio import AsyncIOMotorClient


from app.config import settings

DATABASE_URL = settings.db_url
client = AsyncIOMotorClient(DATABASE_URL, uuidRepresentation="standard")
db = client["irss-test"]
