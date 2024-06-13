from config_data.config import Config, load_config
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
ADMINS: list = config.tg_bot.admin_ids
bot: bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def send_message_to_admin(bot: Bot, text=''):
    for admin in ADMINS:
        await bot.send_message(admin, text=text)
