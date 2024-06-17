import asyncio, random, json, csv, time

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import LinkPreviewOptions, CallbackQuery, Message, ReplyKeyboardRemove
from states import LearningFSM, TestFSM
from utils import send_message_to_admin
from lexicon import *
from db import *
from keyboards import keyboard_builder, main_menu_keyboard

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
        f'\n{MessagesEnum.WELCOME_NEW_USER.value}',
        link_preview_options=LinkPreviewOptions(is_disabled=True))
    await message.answer(MessagesEnum.WELCOME_EXISTING_USER,
                         reply_markup=main_menu_keyboard)
    await send_message_to_admin(message.bot, f"""Зарегистрирован новый пользователь.
Имя: {message.from_user.full_name}\nТелеграм: @{message.from_user.username}\n""")
    await state.set_state(TestFSM.test)


@user_router.message(Command(commands=['main_menu']),
                     ~StateFilter(default_state))  # пользователь зарегистрирован в боте
@user_router.message(Command(commands=['start']), ~StateFilter(default_state))
async def process_start_command_existing_user(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    full_name = message.from_user.full_name
    tg_login = message.from_user.username
    await user_manager.add_user(user_id, full_name, tg_login)
    await message.answer(MessagesEnum.WELCOME_EXISTING_USER.value,
                         reply_markup=main_menu_keyboard)
    await state.set_state(LearningFSM.choose_type_of_exercise)


@user_router.callback_query((F.data == ButtonEnum.MAIN_MENU.value), ~StateFilter(default_state))
async def rules_grammar_training(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(MessagesEnum.WELCOME_EXISTING_USER.value,
                                  reply_markup=main_menu_keyboard)


@user_router.callback_query((F.data == 'Правила грамматика'))
async def rules_grammar_training(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        """Правила простые:\nЯ пишу на русском, ты переводишь на английский.\n\nЕсли ответы не совпадут:
⚪ Можешь попробовать написать предложение ещё раз(количество попыток не ограничено)\n⚪ Можешь поcмотреть ответ, нажав на кнопку «Покажи ответ»""")

    # Grammar Training #


@user_router.callback_query((F.data == ButtonEnum.GRAMMAR_TRAINING.value))  # ,
# StateFilter(LearningFSM.choose_type_of_exercise))
async def start_grammar_training(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отличный выбор!')
    await callback.message.delete()
    await  callback.message.answer(MessagesEnum.GRAMMAR_TRAINING_HELLO,
                                   reply_markup=keyboard_builder(1, **{'Правила грамматика': ButtonEnum.RULES}))
    # await asyncio.sleep(3)
    await callback.message.answer('Выбери раздел:', reply_markup=keyboard_builder(1, *[button.value for button in
                                                                                      GrammarTrainingButtons]))
    await state.set_state(LearningFSM.grammar_choosing_section)


@user_router.callback_query(StateFilter(LearningFSM.grammar_choosing_section))
async def choosing_section_grammar_training(callback: CallbackQuery, state: FSMContext):
    if callback.data in (button.value for button in GrammarTrainingButtons):
        await callback.answer('Хороший выбор 😊')
        await callback.message.delete()
        await callback.message.answer(f"""Ты выбрал раздел \"{callback.data}\"
\nТвой прогресс в этом разделе: {1} из {1}
\nГотов переводить?""", reply_markup=keyboard_builder(1, **{'Готов грамматика': ButtonEnum.READY}))
        await state.set_state(LearningFSM.grammar_choosed_section)
        await state.set_data(callback.data)
    else:
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer(MessagesEnum.ERROR)


@user_router.callback_query((F.data == 'Готов грамматика'))
async def choosed_section_grammar_training(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(f'Переводи следующее:\n{None}')


@user_router.message(Command(commands=["info"]))
async def info_command(message: Message, state: FSMContext):
    await state.set_state(LearningFSM.default)
    await message.answer(MessagesEnum.INFO_RULES.value,
                         reply_markup=keyboard_builder(1, ButtonEnum.MAIN_MENU))


@user_router.message()
async def send_idontknow(message: Message):
    await message.reply(
        f'{message.from_user.first_name}, я всего лишь бот, я не знаю, что на это ответить🤷🏼‍♀'
    )
