
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc


# jobstores = {"mongo": MongoDBJobStore(database="irss-test", client=client)}
executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(5)}
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
