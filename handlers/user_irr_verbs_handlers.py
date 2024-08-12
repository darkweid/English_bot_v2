import asyncio, random, json, csv, time
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import LinkPreviewOptions, CallbackQuery, Message, ReplyKeyboardRemove
from states import IrrVerbsLearningFSM, UserFSM
from utils import send_message_to_admin, update_state_data, time_zones, schedule_reminders
from lexicon import *
from db import *
from keyboards import *

user_irr_verbs_router: Router = Router()
# user_progress_manager = UserProgressManager()
# user_manager = UserManager()
# daily_stats_manager = DailyStatisticsManager()
