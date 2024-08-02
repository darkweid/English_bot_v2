import logging
from aiogram.exceptions import TelegramForbiddenError
from config_data.config import Config, load_config
from aiogram import Bot
from db import UserManager, UserWordsLearningManager
from .bot_init import get_bot_instance
from keyboards import keyboard_builder
from lexicon import BasicButtons, MessageTexts

logger = logging.getLogger(__name__)
config: Config = load_config()
ADMINS: list = config.tg_bot.admin_ids
user_manager: UserManager = UserManager()
user_words_manager: UserWordsLearningManager = UserWordsLearningManager()


async def send_message_to_all_users(text: str):
    """
    Send a message to all users.

    Parameters:
    - text (str): The message text to send.
    """
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
    """
    Send a message to a specific user.

    Parameters:
    - user_id (int): The ID of the user.
    - text (str): The message text to send.
    - learning_button (bool, optional): Whether to include a learning button. Defaults to False.
    """
    bot: Bot = await get_bot_instance()
    try:
        if not learning_button:
            await bot.send_message(user_id, text=text)
        else:
            await bot.send_message(user_id, text=text,
                                   reply_markup=await keyboard_builder(1,
                                                                       learn_new_words=BasicButtons.LEARN_ADDED_WORDS))
    except TelegramForbiddenError as e:
        logger.error(f'Failed to send message to user {user_id}:\n{e}')


async def send_reminder_to_user(user_id: int):
    """
    Send a reminder message to a user about their word learning tasks.

    Parameters:
    - user_id (int): The ID of the user.
    """
    bot: Bot = await get_bot_instance()
    count_words = await user_words_manager.get_count_all_exercises_for_today_by_user(user_id=user_id)
    try:
        if count_words > 0:
            word_form = await get_word_declension(count_words)
            await bot.send_message(user_id, text=MessageTexts.REMINDER_WORDS_TO_LEARN.value.format(word_form),
                                   reply_markup=await keyboard_builder(1,
                                                                       learn_new_words=BasicButtons.LEARN_ADDED_WORDS)
                                   )
        else:
            await bot.send_message(user_id, text=MessageTexts.REMINDER.value)
    except TelegramForbiddenError as e:
        logger.error(f'Failed to send message to user {user_id}:\n{e}')


async def get_word_declension(count: int) -> str:
    """
    Get the correct word declension for the given count.

    Parameters:
    - count (int): The number of words.

    Returns:
    - str: The word form with the correct declension.
    """
    if count % 10 == 1 and count % 100 != 11:
        return f"{count} слово"
    elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
        return f"{count} слова"
    else:
        return f"{count} слов"
