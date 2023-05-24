import asyncio

import feedparser
from fastapi import Request


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
        print(f"Failed to parse feed from {url}: {e}")
        return None, None
