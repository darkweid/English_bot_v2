from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot_instance: Bot = None


async def init_bot_instance(token: str):
    global bot_instance
    if bot_instance is None:
        bot_instance = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def get_bot_instance() -> Bot:
    if bot_instance is None:
        raise Exception("Bot instance is not initialized")
    return bot_instance
