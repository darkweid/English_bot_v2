from config_data.config import Config, load_config
from aiogram import Bot
from .bot_init import get_bot_instance

config: Config = load_config()
ADMINS: list = config.tg_bot.admin_ids


async def send_message_to_admin(text: str, to_super_admin=False):
    bot: Bot = await get_bot_instance()
    if to_super_admin:
        await bot.send_message(ADMINS[0], text=text)
    else:
        for admin in ADMINS:
            await bot.send_message(admin, text=text)
