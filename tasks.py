import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()
from apscheduler.schedulers.blocking import BlockingScheduler
from db.api import send_checked_message_admin

sched = BlockingScheduler(timezone='Asia/Yekaterinburg')


@sched.scheduled_job('cron', hour=0, minute=43)
def timed_job():
    send_checked_message_admin()


# scheduler.add_job(send_checked_message_admin, "cron", day_of_week='mon-sat', hour=12, minute=00)
# scheduler.add_job(send_checked_message_admin, "cron", hour=0, minute=20)
sched.start()
