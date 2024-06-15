import asyncio, logging  # , sqlite_db

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import Config, load_config
from handlers.user_handlers import user_router
from handlers.admin_handlers import admin_router
from keyboards.set_menu import set_main_menu
from utils import send_message_to_admin
from db import init_db

logger = logging.getLogger(__name__)
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
ADMINS: list = config.tg_bot.admin_ids


async def send_message_to_admin(bot: Bot, text=''):
    for admin in ADMINS:
        await bot.send_message(admin, text=text)


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

        bot: bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp: Dispatcher = Dispatcher(storage=storage)

        dp.include_router(admin_router)
        dp.include_router(user_router)
        await set_main_menu(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await send_message_to_admin(bot, text='Бот запущен')
        await dp.start_polling(bot, )
    except Exception as e:
        logger.exception("Ошибка: %s", str(e))

    finally:
        logger.info('Бот был остановлен.')
        await send_message_to_admin(bot, text='Бот остановлен')


if __name__ == "__main__":
    asyncio.run(main())
