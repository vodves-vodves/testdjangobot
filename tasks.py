import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db.settings')
import django
django.setup()
from apscheduler.schedulers.blocking import BlockingScheduler
from db.api import send_checked_message_admin

sched = BlockingScheduler(timezone='Asia/Yekaterinburg')


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=1, minute=23)
def timed_job():
    send_checked_message_admin()


# scheduler.add_job(send_checked_message_admin, "cron", day_of_week='mon-sat', hour=12, minute=00)
# scheduler.add_job(send_checked_message_admin, "cron", hour=0, minute=20)
sched.start()
