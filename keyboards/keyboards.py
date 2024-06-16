from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand, URLInputFile
# from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import ButtonEnum


def keyboard_builder(width: int, *args: list[ButtonEnum], **kwargs: dict[str, ButtonEnum]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

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

    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
