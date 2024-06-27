import asyncio, logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import Config, load_config
from handlers.user_handlers import user_router
from handlers.admin_handlers import admin_router
from keyboards.set_menu import set_main_menu
from utils import send_message_to_admin, scheduler, schedule_reminders, init_bot_instance, get_bot_instance
from db import init_db, ExerciseManager, UserManager, UserProgressManager

logger = logging.getLogger(__name__)
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
ADMINS: list = config.tg_bot.admin_ids

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
        await init_bot_instance(token=BOT_TOKEN)

        bot: Bot = await get_bot_instance()
        dp: Dispatcher = Dispatcher(storage=storage)

        dp.include_router(admin_router)
        dp.include_router(user_router)
        await set_main_menu(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await send_message_to_admin(bot, text='🟢 Бот запущен 🟢')
        await on_startup()
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Ошибка: %s", str(e))

    finally:
        logger.info('Бот был остановлен.')
        await send_message_to_admin(bot, text='🟥 Бот остановлен 🟥')


async def on_startup():
    scheduler.start()
    await schedule_reminders()


if __name__ == "__main__":
    asyncio.run(main())
