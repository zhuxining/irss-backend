from app.core.feed_parser import parse_feed
from app.models.entries import Entry
from app.models.feeds import Feed
from beanie import PydanticObjectId


def should_update_feed() -> bool:
    return False


def should_update_entry() -> bool:
    return False


# async def cm_entry(entryies: list[EntryParser], loop: asyncio.AbstractEventLoop):
#     asyncio.set_event_loop(loop)
#     for entry in entryies:
#         db_entry = Entry(**entry.dict())
#         db_entry.create_time = datetime.utcnow()
#         await Entry.insert_one(db_entry)


async def all_users_entry_append():
    feed_url_list = await Feed.distinct("url")
    for feed_url in feed_url_list:
        feed, entries = await parse_feed(feed_url)
        print(feed_url)
        feed_owner_list = await Feed.find(
            Feed.url == feed_url, Feed.updates_enabled == True  # noqa: E712
        ).to_list()
        for feed_owner in feed_owner_list:
            db_entry_list = []
            entry_list = [Entry(**entry.dict()) for entry in entries]
            for entry in entry_list:
                entry.owner_id = feed_owner.owner_id
                if entry.published > feed_owner.newest_entry_pub_time:
                    db_entry_list.append(entry)
            if db_entry_list != []:
                await Entry.insert_many(db_entry_list)
            await Feed.find(Feed.id == feed_owner.id).update(
                {"$set": {Feed.newest_entry_pub_time: feed.newest_entry_pub_time}}
            )


async def user_entry_append(owner_id: PydanticObjectId):
    feed_owner_list = await Feed.find(Feed.owner_id == owner_id).to_list()
    for feed_owner in feed_owner_list:
        feed, entries = await parse_feed(feed_owner.url)
        db_entry_list = []
        entry_list = [Entry(**entry.dict()) for entry in entries]
        for entry in entry_list:
            entry.owner_id = feed_owner.owner_id
            if entry.published > feed_owner.newest_entry_pub_time:
                db_entry_list.append(entry)
        if db_entry_list != []:
            await Entry.insert_many(db_entry_list)
        await Feed.find(Feed.id == feed_owner.id).update(
            {"$set": {Feed.newest_entry_pub_time: feed.newest_entry_pub_time}}
        )
