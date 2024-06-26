from config_data.config import Config, load_config
from aiogram import Bot

config: Config = load_config()
ADMINS: list = config.tg_bot.admin_ids


async def send_message_to_admin(bot: Bot, text: str, to_super_admin=False):
    if to_super_admin:
        await bot.send_message(ADMINS[0], text=text)
    else:
        for admin in ADMINS:
            await bot.send_message(admin, text=text)
