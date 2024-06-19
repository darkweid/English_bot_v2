import asyncio, random, json, csv, time

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import LinkPreviewOptions, CallbackQuery, Message, ReplyKeyboardRemove
from states import LearningFSM
from utils import send_message_to_admin, update_state_data
from lexicon import *
from db import *
from keyboards import *

user_router: Router = Router()
exercise_manager = ExerciseManager()
user_progress_manager = UserProgressManager()
user_manager = UserManager()


@user_router.message(Command(commands=["reset_fsm"]))
async def resetFSM_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Сброшено!')


@user_router.message(Command(commands=["start"]),
                     StateFilter(default_state))  # стандартное состояние, пользователь не зарегистрирован в боте
async def process_start_command(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    full_name = message.from_user.full_name
    tg_login = message.from_user.username
    await user_manager.add_user(user_id, full_name, tg_login)
    await message.answer(
        f'Привет, {message.from_user.full_name}\nЯ бот от <a href="http://t.me/Oprus">Оли Прус</a>😊'
        f'\n{MessageTexts.WELCOME_NEW_USER.value}',
        link_preview_options=LinkPreviewOptions(is_disabled=True))
    await message.answer(MessageTexts.WELCOME_EXISTING_USER,
                         reply_markup=main_menu_keyboard)
    await send_message_to_admin(message.bot, f"""Зарегистрирован новый пользователь.
Имя: {message.from_user.full_name}\nТелеграм: @{message.from_user.username}\n""")
    await state.set_state(LearningFSM.existing_user)


@user_router.message(Command(commands=['main_menu']),
                     ~StateFilter(default_state))  # пользователь зарегистрирован в боте
@user_router.message(Command(commands=['start']), ~StateFilter(default_state))
async def process_start_command_existing_user(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    full_name = message.from_user.full_name
    tg_login = message.from_user.username
    await user_manager.add_user(user_id, full_name, tg_login)
    await message.answer(MessageTexts.WELCOME_EXISTING_USER.value,
                         reply_markup=main_menu_keyboard)
    await state.set_state(LearningFSM.choose_type_of_exercise)


@user_router.callback_query(F.data == BasicButtons.BACK.value, StateFilter(LearningFSM.testing_choosing_section))
async def main_menu_existing_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(MessageTexts.WELCOME_EXISTING_USER.value,
                                     reply_markup=main_menu_keyboard)
    await state.set_state(LearningFSM.choose_type_of_exercise)


@user_router.callback_query((F.data == BasicButtons.MAIN_MENU.value), ~StateFilter(default_state))
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(MessageTexts.WELCOME_EXISTING_USER.value,
                                  reply_markup=main_menu_keyboard)
    await state.set_state(LearningFSM.default)


@user_router.callback_query((F.data == 'Правила тесты'))
async def rules_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(MessageTexts.INFO_RULES.value,
                                     reply_markup=keyboard_builder(1, BasicButtons.CLOSE))


@user_router.callback_query((F.data == 'Закрыть правила тесты'))
async def close_rules_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()


@user_router.callback_query((F.data == MainMenuButtons.TESTING.value))  # выбор раздела для прохождения теста
async def start_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отличный выбор!')
    await  callback.message.edit_text(MessageTexts.TESTING_HELLO,
                                      reply_markup=keyboard_builder(1, **{'Правила тесты': BasicButtons.RULES,
                                                                          'Закрыть правила тесты': BasicButtons.CLOSE}))
    # await asyncio.sleep(3)
    await callback.message.answer(MessageTexts.CHOOSE_SECTION.value, reply_markup=choose_section_testing_keyboard)
    await state.set_state(LearningFSM.testing_choosing_section)


@user_router.callback_query((F.data == BasicButtons.BACK.value), StateFilter(LearningFSM.testing_choosing_subsection))
async def start_testing(callback: CallbackQuery, state: FSMContext):  # выбор раздела для прохождения тесте
    await callback.answer()
    await callback.message.edit_text(MessageTexts.CHOOSE_SECTION.value, reply_markup=choose_section_testing_keyboard)
    await state.set_state(LearningFSM.testing_choosing_section)


@user_router.callback_query(StateFilter(LearningFSM.testing_choosing_section))  # выбор ПОДраздела для прохождения теста
async def choosing_section_testing(callback: CallbackQuery, state: FSMContext):
    section = testing_section_mapping.get(callback.data)
    if section is None:
        await callback.answer()
        await callback.message.edit_text(MessageTexts.ERROR)
        await state.set_state(LearningFSM.default)
        return

    await callback.message.edit_text(
        MessageTexts.CHOOSE_SUBSECTION_TEST.value,
        reply_markup=keyboard_builder(1, *[button.value for button in section], BasicButtons.BACK,
                                      BasicButtons.MAIN_MENU))
    await state.set_state(LearningFSM.testing_choosing_subsection)
    await update_state_data(state, section=callback.data, subsection=None)
    print(await state.get_data())


@user_router.callback_query(
    StateFilter(LearningFSM.testing_choosing_subsection))  # подраздел выбран, получен в callback
async def choosing_subsection_testing(callback: CallbackQuery, state: FSMContext):
    subsection = callback.data
    data = await state.get_data()
    section = data.get('section')
    await callback.answer()
    await callback.message.edit_text(f"""Отлично, ты выбрал:\n «{section} - {subsection}»\n
Готов проходить?""", reply_markup=keyboard_builder(1, BasicButtons.MAIN_MENU, args_go_first=False,
                                                   ready_for_test=BasicButtons.READY))
    await update_state_data(state, subsection=subsection)
    print(await state.get_data())
    await state.set_state(LearningFSM.testing_choosed_subsection)


@user_router.callback_query((F.data == 'ready_for_test'))
async def choosed_subsection_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(f'Напиши мне чем заполнить пробел в предложении:\n{None}')
    await state.set_state(LearningFSM.testing_in_process)

@user_router.callback_query(StateFilter(LearningFSM.testing_in_process))
async def in_process_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    #здесь если правильно, то хорошо, если нет, то не хорошо))

@user_router.message(Command(commands=["info"]))
async def info_command(message: Message, state: FSMContext):
    await state.set_state(LearningFSM.default)
    await message.answer(MessageTexts.INFO_RULES.value,
                         reply_markup=keyboard_builder(1, BasicButtons.MAIN_MENU))


@user_router.message()
async def send_idontknow(message: Message):
    await message.reply(
        f'{message.from_user.first_name}, я всего лишь бот, я не знаю, что на это ответить🤷🏼‍♀'
    )
