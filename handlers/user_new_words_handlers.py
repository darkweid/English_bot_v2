import asyncio, random, json, csv, time
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import LinkPreviewOptions, CallbackQuery, Message, ReplyKeyboardRemove, User
from states import WordsLearningFSM, UserFSM
from utils import send_message_to_admin, update_state_data, time_zones, schedule_reminders
from lexicon import *
from db import *
from keyboards import *

user_new_words_router: Router = Router()
exercise_manager = ExerciseManager()
user_progress_manager = UserProgressManager()
user_manager = UserManager()


@user_new_words_router.callback_query(F.data == MainMenuButtons.NEW_WORDS.value)
async def start_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отличный выбор!')

    await callback.message.answer('Что хочешь делать?',
                                  reply_markup=await keyboard_builder(1, BasicButtons.MAIN_MENU, args_go_first=False,
                                                                      learn_new_words=BasicButtons.LEARN_ADDED_WORDS,
                                                                      add_new_words=BasicButtons.ADD_WORDS,
                                                                      progress_new_words=BasicButtons.NEW_WORDS_PROGRESS))
    await state.set_state(WordsLearningFSM.default)


@user_new_words_router.callback_query(F.data == 'back_to_main_menu_new_words')
async def start_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отличный выбор!')
    await callback.message.edit_text('Что хочешь делать?',
                                     reply_markup=await keyboard_builder(1, BasicButtons.MAIN_MENU, args_go_first=False,
                                                                         learn_new_words=BasicButtons.LEARN_ADDED_WORDS,
                                                                         add_new_words=BasicButtons.ADD_WORDS,
                                                                         progress_new_words=BasicButtons.NEW_WORDS_PROGRESS))
    await state.set_state(WordsLearningFSM.default)


@user_new_words_router.callback_query(F.data == 'rules_new_words')
async def rules_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(MessageTexts.NEW_WORDS_RULES,
                                     reply_markup=await keyboard_builder(1,
                                                                         more_about_sr=BasicButtons.MORE_ABOUT_SPACED_REPETITION,
                                                                         close_rules_new_words=BasicButtons.CLOSE))


@user_new_words_router.callback_query(F.data == 'more_about_sr')
async def more_about_spaced_repetition_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(MessageTexts.ABOUT_SPACED_REPETITION,
                                     reply_markup=await keyboard_builder(1,
                                                                         close_rules_new_words=BasicButtons.CLOSE))


@user_new_words_router.callback_query(F.data == 'close_rules_new_words')
async def rules_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()


@user_new_words_router.callback_query(F.data == 'learn_new_words')
async def learn_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(MessageTexts.NEW_WORDS_HELLO.value,
                                     reply_markup=await keyboard_builder(1, rules_new_words=BasicButtons.RULES,
                                                                         close_rules_new_words=BasicButtons.CLOSE))
    await callback.message.answer('Здесь будут даваться слова для изучения на сегодня')
    await state.set_state(WordsLearningFSM.in_process)


@user_new_words_router.callback_query(F.data == 'add_new_words')
@user_new_words_router.callback_query(F.data == 'back_to_sections')
async def add_new_words_selecting_section(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(MessageTexts.SELECT_SECTION_WORDS,
                                     reply_markup=await keyboard_builder(1, *[button.value for button in
                                                                              NewWordsSections],
                                                                         back_to_main_menu_new_words=BasicButtons.BACK))
    await state.set_state(WordsLearningFSM.add_words_to_learn)


@user_new_words_router.callback_query(StateFilter(WordsLearningFSM.add_words_to_learn))
async def add_new_words_selected_section(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    section_name = callback.data
    section = new_words_section_mapping.get(section_name)
    if section is None:
        await callback.message.edit_text(MessageTexts.ERROR.value)
        await state.set_state(WordsLearningFSM.default)
        return

    await callback.message.edit_text(
        MessageTexts.SELECT_SUBSECTION_WORDS.value,
        reply_markup=await keyboard_builder(1, *[button.value for button in section],  # subsection buttons
                                            back_to_sections=BasicButtons.BACK,
                                            back_to_main_menu_new_words=BasicButtons.MAIN_MENU_NEW_WORDS))
    await state.set_state(WordsLearningFSM.selecting_subsection)
    await update_state_data(state, section=section_name, subsection=None)


@user_new_words_router.callback_query(StateFilter(WordsLearningFSM.selecting_subsection))
async def add_new_words_selecting_subsection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    subsection = callback.data
    user_data = await state.get_data()
    section = user_data.get('section')
    if subsection is None:
        await callback.message.edit_text(MessageTexts.ERROR.value)
        await state.set_state(UserFSM.default)
        return

    await callback.message.edit_text(f"""Ты выбрал тему {subsection} в разделе {section}
в теме {1} {'идиом' if section == NewWordsSections.IDIOMS.value else 'слов'}
Добавить в изучаемые?""",
                                     reply_markup=await keyboard_builder(1, add_words=BasicButtons.YES,
                                                                         do_not_add_words=BasicButtons.NO,
                                                                         back_to_sections=BasicButtons.BACK,
                                                                         back_to_main_menu_new_words=BasicButtons.MAIN_MENU_NEW_WORDS))
    await state.set_state(WordsLearningFSM.selected_subsection)
    await update_state_data(state, subsection=subsection)


@user_new_words_router.callback_query(StateFilter(WordsLearningFSM.selected_subsection))
async def add_new_words_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_answer = callback.data
    if user_answer == 'add_words':
        # добавить слова в изучение
        await callback.message.edit_text(
            'Добавлено',
            reply_markup=await keyboard_builder(1,
                                                back_to_main_menu_new_words=BasicButtons.MAIN_MENU_NEW_WORDS))
    elif user_answer == 'do_not_add_words':
        await callback.message.edit_text(
            'Слова не добавлены',
            reply_markup=await keyboard_builder(1,
                                                back_to_main_menu_new_words=BasicButtons.MAIN_MENU_NEW_WORDS))
        await update_state_data(state, section=None, subsection=None)


@user_new_words_router.callback_query(F.data == 'progress_new_words')
async def stats_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Здесь будут прогресс',
                                     reply_markup=await keyboard_builder(1,
                                                                         back_to_main_menu_new_words=BasicButtons.BACK))
