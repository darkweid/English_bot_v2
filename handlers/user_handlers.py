import asyncio, random, json, csv, time

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from states import LearningFSM
from utils import send_message_to_admin



user_router: Router = Router()


@user_router.message(Command(commands=["start"]), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await send_message_to_admin(message.bot, 'превед')
    await message.answer('Привет!')
