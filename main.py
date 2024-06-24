import asyncio, logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import Config, load_config
from handlers.user_handlers import user_router
from handlers.admin_handlers import admin_router
from keyboards.set_menu import set_main_menu
from utils import send_message_to_admin
from lexicon import MessageTexts
from db import init_db, ExerciseManager, UserManager, UserProgressManager

logger = logging.getLogger(__name__)
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
ADMINS: list = config.tg_bot.admin_ids

scheduler = AsyncIOScheduler()
exercise_manager = ExerciseManager()
user_progress_manager = UserProgressManager()
user_manager = UserManager()


async def main():
    try:
        logging.basicConfig(  # filename='bot.log',
            level=logging.INFO,
            format='#%(levelname)-8s '
                   '[%(asctime)s] - %(name)s - %(message)s')

        logger.info('Starting bot')

        redis: Redis = Redis(host='localhost')

        storage: RedisStorage = RedisStorage(redis=redis)

        await init_db()
        await exercise_manager.init_tables()
        await user_progress_manager.init_tables()
        await user_manager.init_tables()

        bot: bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp: Dispatcher = Dispatcher(storage=storage)

        dp.include_router(admin_router)
        dp.include_router(user_router)
        await set_main_menu(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await send_message_to_admin(bot, text='🟢 Бот запущен 🟢')
        await dp.start_polling(bot, )
    except Exception as e:
        logger.exception("Ошибка: %s", str(e))

    finally:
        logger.info('Бот был остановлен.')
        await send_message_to_admin(bot, text='🟥 Бот остановлен 🟥')


async def send_reminder(bot: Bot, user_id):
    await bot.send_message(user_id, text=MessageTexts.REMINDER.value)


async def schedule_reminders(bot):
    users = await user_manager.get_all_users()
    scheduler.remove_all_jobs()
    for user in users:
        reminder_time = user.get('reminder_time')
        user_tz_offset = user.get('time_zone')
        user_id = user.get('user_id')
        if reminder_time and user_tz_offset:
            user_tz = timezone(timedelta(hours=int(user_tz_offset)))
            scheduler.add_job(func=send_reminder, trigger='cron',
                              hour=reminder_time.hour, minute=reminder_time.minute,
                              timezone=user_tz,
                              kwargs={'user_id': user_id, 'bot': bot})
if __name__ == "__main__":
    asyncio.run(main())
