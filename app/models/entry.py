from datetime import datetime
from typing import Any, Set, Union
from uuid import UUID, uuid4

import pymongo
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from pymongo import IndexModel


class Entry(Document):
    #: The entry id.
    uid: UUID = Field(default_factory=uuid4)

    #: The date the entry was last updated, according to the feed.

    updated: datetime | None = None

    #: The title of the entry.
    title: str | None = None

    #: The URL of a page associated with the entry.
    link: str | None = None

    #: The author of the feed.
    author: str | None = None

    #: The date the entry was published, according to the feed.
    published: datetime | None = None

    #: A summary of the entry.
    summary: str | None = None

    #: Full content of the entry.
    #: A sequence of :class:`Content` objects.
    summary_detail: object

    #: External files associated with the entry.
    #: A sequence of :class:`Enclosure` objects.
    enclosures: str | None = None

    #: Whether the entry was read or not.
    read: bool = False

    #: The date when :attr:`read` was last set by the user;
    #: :const:`None` if that never happened,
    #: or the entry predates the date being recorded.

    read_modified: datetime | None = None

    #: Whether the entry is important or not.
    #: :const:`None` means not set.
    #: :const:`False` means "explicitly unimportant".
    #:  :attr:`important` is now an optional :class:`bool`,
    #:  and defaults to :const:`None`.
    important: bool | None = None

    #: The date when :attr:`important` was last set by the user;
    #: :const:`None` if that never happened,
    #: or the entry predates the date being recorded.

    important_modified: datetime | None = None

    #: The date when the entry was added (first updated) to reader.

    added: datetime
    #: The source of the entry. One of ``'feed'``, ``'user'``.
    #:
    #: Other values may be added in the future.

    added_by: object

    #: The date when the entry was last updated by reader.
    last_updated: datetime = Field(default_factory=datetime.now)

    #: The URL of the original feed of the entry.
    original_feed: object

    # feed should not have a default, but I'd prefer objects that aren't
    # entry data to be at the end, and dataclasses don't support keyword-only
    # arguments yet.
    #
    # We could use a null object as the default (Feed('')), but None
    # increases the chance we'll catch feed= not being set at runtime;
    # we don't check for it in __post_init__ because it's still useful
    # to have it None in tests. The cast is to please mypy.

    #: The entry's feed.

    class Settings:
        name = "entry"
        indexes = [
            IndexModel([("uid", pymongo.DESCENDING)], unique=True),
            IndexModel([("title", pymongo.ASCENDING)], unique=False),
            IndexModel([("published", pymongo.ASCENDING)], unique=False),
            IndexModel(
                [
                    ("title", pymongo.TEXT),
                    ("subtitle", pymongo.TEXT),
                    ("user_title", pymongo.TEXT),
                    ("author", pymongo.TEXT),
                ],
                name="text_index",
            ),
        ]
