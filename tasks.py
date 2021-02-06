import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db.settings')
from apscheduler.schedulers.blocking import BlockingScheduler
from db.api import send_checked_message_admin


scheduler = BlockingScheduler(timezone='Asia/Yekaterinburg')
# scheduler.add_job(send_checked_message_admin, "cron", day_of_week='mon-sat', hour=12, minute=00)
scheduler.add_job(send_checked_message_admin, "cron", hour=0, minute=20)
scheduler.start()