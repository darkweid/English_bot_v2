import asyncio, random, json, csv, time

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from states import AdminFSM
from db import ExerciseManager, UserProgressManager

admin_router: Router = Router()
exercise_manager = ExerciseManager('english_bot.db')
user_progress_manager = UserProgressManager('english_bot.db')