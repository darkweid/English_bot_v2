import logging
from aiogram.exceptions import TelegramForbiddenError
from config_data.config import Config, load_config
from aiogram import Bot
from db import UserManager
from .bot_init import get_bot_instance
from keyboards import keyboard_builder
from lexicon import BasicButtons

config: Config = load_config()
ADMINS: list = config.tg_bot.admin_ids
user_manager: UserManager = UserManager()
user_words_manager: UserWordsLearningManager = UserWordsLearningManager()


async def send_message_to_all_users(text: str):
    bot: Bot = await get_bot_instance()
    if bot is None:
        raise Exception('Bot instance is not available')
    users = await user_manager.get_all_users()
    for user in users:
        user_id = user.get('user_id')
        try:
            await bot.send_message(user_id, text=text)
        except TelegramForbiddenError as e:
            logger.error(f'Failed to send broadcast message to user {user_id}:\n{e}')


async def send_message_to_user(user_id: int, text: str, learning_button: bool = False):
    bot: Bot = await get_bot_instance()
    if not learning_button:
        await bot.send_message(user_id, text=text)
    else:
        await bot.send_message(user_id, text=text,
                               reply_markup=await keyboard_builder(1, learn_new_words=BasicButtons.LEARN_ADDED_WORDS))
    try:
        if not learning_button:
            await bot.send_message(user_id, text=text)
        else:
            await bot.send_message(user_id, text=text,
                                   reply_markup=await keyboard_builder(1,
                                                                       learn_new_words=BasicButtons.LEARN_ADDED_WORDS))
    except TelegramForbiddenError as e:
        logger.error(f'Failed to send message to user {user_id}:\n{e}')


