import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db.settings')
import django

django.setup()
from apscheduler.schedulers.blocking import BlockingScheduler
from db.api import send_checked_message_admin, mailing, add_excel

sched = BlockingScheduler(timezone='Asia/Yekaterinburg')


@sched.scheduled_job('cron', day_of_week='mon-sat', hour=12, minute=00)
def timed_job():
    send_checked_message_admin()


@sched.scheduled_job('cron', day_of_week='mon-sat', hour=9, minute=10)
def timed_notif():
    mailing()

@sched.scheduled_job('cron', day_of_week='mon-sat', hour=1, minute=40)
def send_excel():
    add_excel()


# scheduler.add_job(send_checked_message_admin, "cron", day_of_week='mon-sat', hour=12, minute=00)
# scheduler.add_job(send_checked_message_admin, "cron", hour=0, minute=20)
sched.start()
