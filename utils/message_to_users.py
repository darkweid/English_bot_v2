from config_data.config import Config, load_config
from aiogram import Bot
from db import UserManager

config: Config = load_config()
ADMINS: list = config.tg_bot.admin_ids
user_manager: UserManager = UserManager()


async def send_message_to_all_users(bot: Bot, text: str):
    users = user_manager.get_all_users()
    for user in users:
        user_id = user.get('user_id')
        await bot.send_message(user_id, text=text)


async def send_message_to_user(bot: Bot, user_id: int, text: str):
    await bot.send_message(user_id, text=text)
