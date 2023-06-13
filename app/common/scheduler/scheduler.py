from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from app.core.entry_append import get_feed_to_update

# jobstores = {"mongo": MongoDBJobStore(database="irss-test", client=client)}
executors = {"default": AsyncIOExecutor()}
job_defaults = {"coalesce": False, "max_instances": 3}
scheduler = AsyncIOScheduler(
    # jobstores=jobstores,
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
    func=get_feed_to_update,
    trigger="interval",
    seconds=10,
)
