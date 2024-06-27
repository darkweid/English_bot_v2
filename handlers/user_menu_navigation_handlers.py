from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from states import LearningFSM
from lexicon import BasicButtons, MessageTexts, MainMenuButtons
from keyboards import keyboard_builder

user_navigation_router: Router = Router()


@user_navigation_router.callback_query(F.data == BasicButtons.CLOSE.value)
async def close_message(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()


@user_navigation_router.callback_query((F.data == BasicButtons.MAIN_MENU.value), ~StateFilter(default_state))
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(MessageTexts.WELCOME_EXISTING_USER.value,
                                  reply_markup=await keyboard_builder(1, *[button.value for button in MainMenuButtons]))
    await state.set_state(LearningFSM.default)


@user_navigation_router.callback_query(F.data == BasicButtons.BACK.value,
                                       StateFilter(LearningFSM.testing_choosing_section))
async def main_menu_existing_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(MessageTexts.WELCOME_EXISTING_USER.value,
                                     reply_markup=await keyboard_builder(1,
                                                                         *[button.value for button in MainMenuButtons]))
    await state.set_state(LearningFSM.choose_type_of_exercise)
