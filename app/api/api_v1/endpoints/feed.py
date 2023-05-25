from datetime import datetime

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import Response
from pydantic import HttpUrl, Json

from app.common.response import resp, state
from app.core.feed_parser import parse_feed
from app.core.users import current_active_user
from app.items_example import crud, model, schema
from app.models.users import User
from app.schemas.feeds import FeedBase, FeedCreate
from app.utils.tools_func import paginated_find
from app.crud.feeds import create_feed

router = APIRouter()


@router.get("/parser/")
async def parser_url(url: HttpUrl) -> Response:
    feed, entries = await parse_feed(url)
    return resp.result(state.Ok, data=entries)


@router.get("/parser0/")
async def parser_url_feed(url: HttpUrl) -> Response:
    feed, entries = await parse_feed(url)
    return resp.result(state.Ok, data=feed)


@router.get("/parser1/")
async def parser_url_entry(url: HttpUrl) -> Response:
    feed, entries = await parse_feed(url)
    return resp.result(state.Ok, data=entries)


@router.get("/parser2/")
async def create(url: HttpUrl, display_title: str) -> Response:
    feed, entries = await parse_feed(url)
    db_feed = FeedCreate(**feed.dict())
    db_feed.display_title = display_title
    db_data = await create_feed(db_feed)
    return resp.result(state.Ok, data=db_data)
