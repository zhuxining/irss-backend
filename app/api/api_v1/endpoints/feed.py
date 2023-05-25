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
from app.schemas.feeds import FeedBase
from app.utils.tools_func import paginated_find
from app.crud.feeds import create_feed

router = APIRouter()


@router.get("/parser/")
async def parser_url(url: str) -> Response:
    db_data = await parse_feed(url)
    return resp.result(state.Ok, data=db_data)


@router.get("/parser0/")
async def parser_url_feed(url: str) -> Response:
    db_data = await parse_feed(url)
    return resp.result(state.Ok, data=db_data[0])


@router.get("/parser1/")
async def parser_url_entry(url: str) -> Response:
    db_data = await parse_feed(url)
    return resp.result(state.Ok, data=db_data[1])


@router.get("/parser2/")
async def create(url: str):
    feed_parse_data = await parse_feed(url)
    db_data = await create_feed(feed_parse_data[0])
    return resp.result(state.Ok, data=db_data)
