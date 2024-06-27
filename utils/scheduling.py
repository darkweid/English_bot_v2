from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from datetime import timedelta, timezone, datetime

from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from utils import send_message_to_user, send_message_to_all_users
from db import UserManager
from lexicon import MessageTexts

user_manager = UserManager()

jobstores = {
    'reminders': MemoryJobStore(),
    'broadcasts': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

scheduler = AsyncIOScheduler(jobstores=jobstores)


async def schedule_reminders():
    users = await user_manager.get_all_users()
    scheduler.remove_all_jobs(jobstore='reminders')
    for user in users:
        username = user.get('tg_login')
        reminder_time = user.get('reminder_time')
        user_tz_offset = user.get('time_zone')
        user_id = user.get('user_id')
        if reminder_time and user_tz_offset:
            user_tz = timezone(timedelta(hours=int(user_tz_offset)))
            scheduler.add_job(func=send_message_to_user, trigger='cron',
                              hour=reminder_time.hour, minute=reminder_time.minute,
                              timezone=user_tz,
                              kwargs={'user_id': user_id, 'text': MessageTexts.REMINDER.value},
                              jobstore='reminders', name=f'Reminder for @{username} ({user_id})')


async def schedule_broadcast(date_time: datetime, text: str):
    tz = timezone(timedelta(hours=3))
    date_time = date_time.replace(tzinfo=tz)
    trigger = DateTrigger(run_date=date_time)
    scheduler.add_job(func=send_message_to_all_users, trigger=trigger,
                      kwargs={'text': text},
                      jobstore='broadcasts', name=f'Broadcast {date_time.strftime("%H:%M (UTC+3) %d.%m.%Y")}')


async def delete_scheduled_broadcasts():
    scheduler.remove_all_jobs(jobstore='broadcasts')
