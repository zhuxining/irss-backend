from datetime import datetime
from typing import List

import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BaseOAuthAccount, BeanieBaseUser, BeanieUserDatabase
from pydantic import Field


class OAuthAccount(BaseOAuthAccount):
    pass


class User(BeanieBaseUser, Document):
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)
    create_time: datetime = Field(default_factory=datetime.utcnow)


async def get_user_db():
    yield BeanieUserDatabase(User, OAuthAccount)  # type: ignore
