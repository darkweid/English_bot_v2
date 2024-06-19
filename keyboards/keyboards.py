from typing import Union
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand, URLInputFile
# from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import *

ButtonEnumType = Union[BasicButtons, MainMenuButtons, AdminMenuButtons, TestingSections, MessageTexts, TensesSections,
ConstructionsSections, PhrasesAndWordsSections, PrepositionsSections, ModalVerbsSections,
ConditionalsSections]


def keyboard_builder(width: int, *args: ButtonEnumType, args_go_first: bool = True,
                     **kwargs: dict[str, ButtonEnumType]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if args_go_first:
        if args:
            for button in args:
                buttons.append(InlineKeyboardButton(
                    text=button,
                    callback_data=button))

        if kwargs:
            for callback, button in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=button,
                    callback_data=callback))
    else:
        if kwargs:
            for callback, button in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=button,
                    callback_data=callback))
        if args:
            for button in args:
                buttons.append(InlineKeyboardButton(
                    text=button,
                    callback_data=button))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


main_menu_keyboard: InlineKeyboardMarkup = keyboard_builder(1, *[button.value for button in MainMenuButtons])
choose_section_testing_keyboard: InlineKeyboardMarkup = keyboard_builder(1, *[button.value for button in
                                                                              TestingSections], BasicButtons.BACK,
                                                                         BasicButtons.MAIN_MENU)
