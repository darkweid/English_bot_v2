import asyncio, random, json, csv, time

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram import Router, F, Bot
from config_data.config import Config, load_config
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from states import AdminFSM, LearningFSM
from db import ExerciseManager, UserProgressManager
from keyboards import *
from lexicon import AdminMenuButtons, GrammarTrainingButtons

admin_router: Router = Router()
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
ADMINS: list = config.tg_bot.admin_ids


@admin_router.message(Command(commands=["admin"]))
async def admin_command(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer('🔘 Привет, что будем делать? 🔘',
                             reply_markup=keyboard_builder(1, AdminMenuButtons.EXERCISES,
                                                           AdminMenuButtons.SEE_ACTIVITY_DAY,
                                                           AdminMenuButtons.SEE_ACTIVITY_WEEK,
                                                           AdminMenuButtons.USERS, AdminMenuButtons.EXIT))
        await state.set_state(AdminFSM.default)
    else:
        await message.answer('🚫 Вам сюда нельзя 🚫')


@admin_router.callback_query((F.data == AdminMenuButtons.EXIT.value))
async def admin_exit(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer('До скорых встреч 👋')
    await state.set_state(LearningFSM.default)


@admin_router.callback_query((F.data == AdminMenuButtons.EXERCISES.value), StateFilter(AdminFSM.default))
async def admin_exercises(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выбери группу упражнений:',
                                     reply_markup=keyboard_builder(1, **{'Грамматика админ': AdminMenuButtons.GRAMMAR,
                                                                         'Новые слова админ': AdminMenuButtons.NEW_WORDS,
                                                                         'Неправильные глаголы админ': AdminMenuButtons.IRR_VERBS}))


@admin_router.callback_query((F.data == 'Грамматика админ'))
async def admin_choose_type_of_exercise(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Выбери раздел упражнений:',
                                     reply_markup=keyboard_builder(1, *([button.value for button in
                                                                         GrammarTrainingButtons] + [
                                                                            AdminMenuButtons.BACK,
                                                                            AdminMenuButtons.EXIT])))
    await state.set_state(AdminFSM.choose_type_of_exercise_grammar)


@admin_router.callback_query(StateFilter(AdminFSM.choose_type_of_exercise_grammar))
async def admin_choosed_type_of_exercise(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(f'Выбран раздел \"{callback.data}\"\n\nЧто нужно сделать?',
                                     reply_markup=keyboard_builder(1, AdminMenuButtons.SEE_EXERCISES_GRAMMAR,
                                                                   AdminMenuButtons.ADD_EXERCISE_GRAMMAR,
                                                                   AdminMenuButtons.DEL_EXERCISE_GRAMMAR,
                                                                   AdminMenuButtons.BACK,
                                                                   AdminMenuButtons.EXIT))
    await state.set_data(callback.data)
    await state.set_state(AdminFSM.choose_what_to_do_with_exercise_grammar)


@admin_router.callback_query(F.data == AdminMenuButtons.SEE_EXERCISES_GRAMMAR.value)
@admin_router.callback_query(F.data == AdminMenuButtons.ADD_EXERCISE_GRAMMAR.value)
@admin_router.callback_query(F.data == AdminMenuButtons.DEL_EXERCISE_GRAMMAR.value)
async def admin_grammar_management(callback: CallbackQuery, state: FSMContext):
    section = await state.get_data()
    if callback.data == AdminMenuButtons.SEE_EXERCISES_GRAMMAR.value:
        await callback.message.edit_text(f'Вот все предложения из раздела\n\"{section}\":',
                                         reply_markup=keyboard_builder(1, AdminMenuButtons.BACK,
                                                                       AdminMenuButtons.EXIT))
    elif callback.data == AdminMenuButtons.ADD_EXERCISE_GRAMMAR.value:
        await callback.message.edit_text(f"""Введи предложения для добавления в раздел\n\"{section}\"
В формате: \nПредложение на русском=+=English sentence""",
                                         reply_markup=keyboard_builder(1, AdminMenuButtons.BACK,
                                                                       AdminMenuButtons.EXIT))
        await state.set_state(AdminFSM.adding_sentence_grammar)
    elif callback.data == AdminMenuButtons.DEL_EXERCISE_GRAMMAR.value:
        await callback.message.edit_text(f'Введи номер предложения для удаления из\n\"{section}\"',
                                         reply_markup=keyboard_builder(1, AdminMenuButtons.BACK,
                                                                       AdminMenuButtons.EXIT))
