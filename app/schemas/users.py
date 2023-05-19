from datetime import datetime

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[PydanticObjectId]):
    create_time: datetime


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
