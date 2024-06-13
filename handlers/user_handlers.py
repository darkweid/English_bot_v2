import asyncio, random, json, csv, time

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from states import LearningFSM
from utils import send_message_to_admin
from db import ExerciseManager, UserProgressManager



user_router: Router = Router()
# Создаем менеджеров базы данных
exercise_manager = ExerciseManager('english_bot.db')
user_progress_manager = UserProgressManager('english_bot.db')


@user_router.message(Command(commands=["start"]), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await send_message_to_admin(message.bot, 'превед')
    await message.answer('Привет!')
