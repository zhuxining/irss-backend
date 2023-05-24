import asyncio

import feedparser
from fastapi import Request
from app.common.logger import log


def is_valid_rss(url) -> bool:
    try:
        feed = feedparser.parse(url)
        if len(feed.entries) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Failed to parse RSS from {url}: {e}")
        return False


async def parse_feed(url):
    try:
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(None, feedparser.parse, url)
        feed = await asyncio.wait_for(future, timeout=10)
        entries = feed.entries
        return feed, entries
    except asyncio.TimeoutError:
        print(f"Timed out while parsing feed from {url}")
        return None, None
    except Exception as e:
        log.debug(f"Failed to parse feed from {url}: {e}")
        return None, None


d = feedparser.parse("https://www.ithome.com/rss/")

print(d.bozo)
