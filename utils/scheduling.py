from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta, timezone


from utils import send_message_to_user
from db import UserManager
from lexicon import MessageTexts

user_manager = UserManager()
scheduler = AsyncIOScheduler()


async def schedule_reminders(bot: Bot):
    users = await user_manager.get_all_users()
    scheduler.remove_all_jobs()
    for user in users:
        reminder_time = user.get('reminder_time')
        user_tz_offset = user.get('time_zone')
        user_id = user.get('user_id')
        if reminder_time and user_tz_offset:
            user_tz = timezone(timedelta(hours=int(user_tz_offset)))
            scheduler.add_job(func=send_message_to_user, trigger='cron',
                              hour=reminder_time.hour, minute=reminder_time.minute,
                              timezone=user_tz,
                              kwargs={'user_id': user_id, 'bot': bot, 'text': MessageTexts.REMINDER.value})
