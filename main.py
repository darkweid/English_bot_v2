import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import Config, load_config
from handlers import *
from keyboards.set_menu import set_main_menu
from utils import send_message_to_admin, scheduler, schedule_reminders, init_bot_instance, get_bot_instance
from db import init_db

logging.basicConfig(  # filename='bot.log',
    level=logging.INFO,
    format='#%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')
logger = logging.getLogger(__name__)
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.setLevel(logging.INFO)

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
REDIS_DSN: str = config.tg_bot.redis_dsn
ADMINS: list = config.tg_bot.admin_ids


async def main():
    try:
        logger.info('Starting bot')

        # redis: Redis = Redis(host='localhost')
        # storage: RedisStorage = RedisStorage(redis=redis)
        storage = RedisStorage.from_url(url=REDIS_DSN)

        await init_db()
        await init_bot_instance(token=BOT_TOKEN)

        bot: Bot = await get_bot_instance()
        dp: Dispatcher = Dispatcher(storage=storage)

        dp.include_router(user_commands_router)
        dp.include_router(admin_router)

        dp.include_router(user_navigation_router)
        dp.include_router(user_stats_router)
        dp.include_router(user_reminder_router)
        dp.include_router(user_testing_router)
        dp.include_router(user_irr_verbs_router)
        dp.include_router(user_new_words_router)
        dp.include_router(fallback_router)

        await set_main_menu(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await send_message_to_admin(text='🟢 Бот запущен 🟢')
        await on_startup()
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Ошибка: %s", str(e))

    finally:
        logger.info('Бот был остановлен.')
        await send_message_to_admin(text='🟥 Бот остановлен 🟥')


async def on_startup():
    scheduler.start()
    await schedule_reminders()


if __name__ == "__main__":
    asyncio.run(main())
