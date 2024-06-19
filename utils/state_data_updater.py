from aiogram.fsm.context import FSMContext
from enum import Enum


async def update_state_data(state: FSMContext, **kwargs):
    """
    Обновляет данные в состоянии с помощью предоставленных ключей и значений.

    :param state: Текущий объект состояния FSMContext.
    :param kwargs: Ключи и значения, которые нужно добавить или обновить в данных состояния.
    """
    data = await state.get_data()

    for key, value in kwargs.items():
        if isinstance(value, Enum):
            kwargs[key] = value.name

    data.update(kwargs)

    await state.set_data(data)



