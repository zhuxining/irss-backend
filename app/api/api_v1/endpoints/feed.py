from datetime import datetime

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import Response
from pydantic import Json

from app.common.response import resp, state
from app.core.feed_parser import parse_feed
from app.core.users import current_active_user
from app.items_example import crud, model, schema
from app.models.users import User
from app.utils.tools_func import paginated_find

router = APIRouter()


@router.get("/parser/")
async def parser_url(url: str) -> Response:
    db_data = await parse_feed(url)
    return resp.result(state.Ok, data=db_data)


@router.get("/parser1/")
async def is_valid_rss(url: str):
    db_data = await is_valid_rss(url)
    return resp.result(state.Ok, data=db_data)
