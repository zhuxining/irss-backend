from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from app.core.entry_append import all_users_entry_append

executors = {"default": AsyncIOExecutor()}
job_defaults = {"coalesce": False, "max_instances": 3}
scheduler = AsyncIOScheduler(
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc,
)


# @scheduler.scheduled_job("interval", seconds=5)
# def timed_task():
#     print("This job is run every five seconds.")

# scheduler.add_job(
#     func=my_job,
#     trigger="interval",
#     seconds=5,
# )

scheduler.add_job(
    func=all_users_entry_append,
    trigger="interval",
    max_instances=4,
    misfire_grace_time=None,
    minutes=30,
    # seconds=10,
)
