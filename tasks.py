from apscheduler.schedulers.blocking import BlockingScheduler
from db.api import send_checked_message_admin


scheduler = BlockingScheduler(timezone='Asia/Yekaterinburg')
# scheduler.add_job(send_checked_message_admin, "cron", day_of_week='mon-sat', hour=12, minute=00)
scheduler.add_job(send_checked_message_admin, "cron", day_of_week='mon-sat', hour=23, minute=55)
scheduler.start()