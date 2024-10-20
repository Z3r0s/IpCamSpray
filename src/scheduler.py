from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from src.request_handler import pspray

def schedule_task(start_time, end_time, target_url, creds_file, use_proxies, model_name):
    scheduler = AsyncIOScheduler()
    start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")

    # Schedule the start of the spraying process
    scheduler.add_job(pspray, 'date', run_date=start, args=[target_url, creds_file, use_proxies, model_name])
    # Stop the spraying at the specified end time by cancelling all tasks
    scheduler.add_job(scheduler.shutdown, 'date', run_date=end)

    print(f"Scheduled task to start at {start} and stop at {end}")
    scheduler.start()