from config_data.config import Config, load_config
from aiogram import Bot
from db import UserManager
from .bot_init import get_bot_instance

config: Config = load_config()
ADMINS: list = config.tg_bot.admin_ids
user_manager: UserManager = UserManager()


async def send_message_to_all_users(text: str):
    bot: Bot = await get_bot_instance()
    if bot is None:
        raise Exception('Bot instance is not available')
    users = await user_manager.get_all_users()
    for user in users:
        user_id = user.get('user_id')
        await bot.send_message(user_id, text=text)


async def send_message_to_user(user_id: int, text: str):
    bot: Bot = await get_bot_instance()
    await bot.send_message(user_id, text=text)
