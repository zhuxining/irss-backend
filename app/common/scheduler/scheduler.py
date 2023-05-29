import os
import sys
from datetime import datetime, timedelta

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from app.common.db.database import client, db

# jobstores = {"mongo": MongoDBJobStore(database="irss-test", client=client)}
executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(5)}
job_defaults = {"coalesce": False, "max_instances": 3}
scheduler = AsyncIOScheduler(
    # jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc,
)


@scheduler.scheduled_job("interval", seconds=5)
def timed_task():
    print("This job is run every five seconds.")
