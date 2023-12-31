import asyncio
import urllib.parse
from datetime import datetime
from typing import Any

import feedparser
from pydantic import HttpUrl

from app.common.logger import log
from app.common.response import state
from app.schemas.entries import Content, Enclosures, EntryParser
from app.schemas.feeds import FeedParser
from app.utils.time_util import strutc_to_datetime


def get_datetime_attr(thing: Any, key: str) -> datetime | None:
    value = thing[key] if key in thing else None
    return strutc_to_datetime(value) if value else None


def process_entry(feed_url: HttpUrl, entry: Any) -> EntryParser:
    content = []
    for data in entry.get("content", ()):
        data = {k: v for k, v in data.items() if k in ("value", "type", "language")}
        content.append(Content(**data))

    enclosures = []
    for data in entry.get("enclosures", ()):
        data = {k: v for k, v in data.items() if k in ("href", "type", "length")}
        href = data.get("href")
        if not href:
            continue
        if "length" in data:
            try:
                data["length"] = int(data["length"])
            except (TypeError, ValueError):
                del data["length"]
        enclosures.append(Enclosures(**data))

    entry_published_time = get_datetime_attr(entry, "published_parsed")
    entry_updated_time = get_datetime_attr(entry, "updated_parsed")
    now_time = datetime.utcnow()

    published = (
        entry_published_time
        if entry_published_time
        else entry_updated_time
        if entry_updated_time
        else now_time
    )

    entry = EntryParser(
        feed_url=feed_url,
        title=entry.get("title"),
        link=entry.get("link"),
        published=published,
        summary=entry.get("summary"),
        content=content,
        enclosures=enclosures,
    )

    return entry


SURVIVABLE_EXCEPTION_TYPES = (
    feedparser.CharacterEncodingOverride,
    feedparser.NonXMLContentType,
)


async def parse_feed(url) -> tuple[FeedParser, list[EntryParser]]:
    url = url.lower()
    try:
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(None, feedparser.parse, url)
        d = await asyncio.wait_for(future, timeout=6)
        if d.get("bozo"):
            exception = d.get("bozo_exception")
            if isinstance(exception, SURVIVABLE_EXCEPTION_TYPES):
                log.info(f"parse {url}: got {exception}")
                raise state.BusinessError.set_msg("Rss地址错误,请检查URL后重试")
            else:
                log.info(f"parse {url}: error while parsing feed")
                raise state.BusinessError.set_msg("Rss地址错误,请检查URL后重试")

        if not d.version:
            log.info(f"parse {url}: unknown feed type")
            raise state.BusinessError.set_msg("unknown feed type")

        if d.feed.get("link").startswith("http://") or d.feed.get("link").startswith(
            "https://"
        ):
            url_parts = urllib.parse.urlparse(d.feed.get("link"))
            link = url_parts.scheme + "://" + url_parts.netloc
        else:
            url_parts = urllib.parse.urlparse(url)
            link = url_parts.scheme + "://" + url_parts.netloc

        feed = FeedParser(
            url=url,
            updated=get_datetime_attr(d.feed, "updated_parsed"),
            title=d.feed.get("title"),
            link=link,
            author=d.feed.get("author"),
            subtitle=d.feed.get("subtitle"),
            version=(d.version).lower(),
            logo_url=link + "/favicon.ico",
            newest_entry_pub_time=datetime.utcnow(),
        )
        entries: list[EntryParser] = []

        entry_published_time = get_datetime_attr(d.entries[0], "published_parsed")
        entry_updated_time = get_datetime_attr(d.entries[0], "updated_parsed")
        now_time = datetime.utcnow()
        entry_pub_time = (
            entry_published_time
            if entry_published_time
            else entry_updated_time
            if entry_updated_time
            else now_time
        )

        for e in d.entries:
            entry = process_entry(url, e)
            entries.append(entry)

            if entry.published >= entry_pub_time:
                entry_pub_time = entry.published

        feed.newest_entry_pub_time = entry_pub_time
        return feed, entries

    except asyncio.TimeoutError:
        log.info(f"Timed out while parsing feed from {url}")
        raise state.BusinessError.set_msg("解析Rss地址超时，请检查URL是否正确后重试")
    except Exception as e:
        log.info(f"Failed to parse feed from {url}: {e}")
        raise e
