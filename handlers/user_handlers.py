import asyncio, random, json, csv, time

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import LinkPreviewOptions, CallbackQuery, Message, ReplyKeyboardRemove
from states import LearningFSM
from utils import send_message_to_admin
from db import ExerciseManager, UserProgressManager
from lexicon import LEXICON_RU

user_router: Router = Router()
exercise_manager = ExerciseManager('english_bot.db')
user_progress_manager = UserProgressManager('english_bot.db')


@user_router.message(Command(commands=["start"]), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.full_name}\nЯ бот от <a href="http://t.me/Oprus">Оли Прус</a> :)',
                         link_preview_options=LinkPreviewOptions(is_disabled=True))
    await message.answer(LEXICON_RU["welcome"])
    await send_message_to_admin(message.bot, f"""Зарегистрирован новый пользователь.
Имя: {message.from_user.full_name}\nТелеграм: @{message.from_user.username}\n""")
