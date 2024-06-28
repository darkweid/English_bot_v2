import asyncio
import random
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from states import TestingFSM
from utils import send_message_to_admin, update_state_data
from lexicon import (MessageTexts, BasicButtons, TestingSections, MainMenuButtons, list_right_answers,
                     testing_section_mapping)
from db import ExerciseManager, UserProgressManager
from keyboards import keyboard_builder

user_testing_router: Router = Router()

exercise_manager = ExerciseManager()
user_progress_manager = UserProgressManager()


@user_testing_router.callback_query((F.data == 'rules_testing'))
async def rules_testing(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(MessageTexts.TEST_RULES.value,
                                     reply_markup=await keyboard_builder(1, close_rules_tests=BasicButtons.CLOSE))


@user_testing_router.callback_query((F.data == 'close_rules_tests'))
async def close_rules_testing(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()


@user_testing_router.callback_query((F.data == MainMenuButtons.TESTING.value))  # выбор раздела для прохождения теста
async def start_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отличный выбор!')
    await callback.message.edit_text(MessageTexts.TESTING_HELLO.value,
                                     reply_markup=await keyboard_builder(1, rules_testing=BasicButtons.RULES,
                                                                         close_rules_tests=BasicButtons.CLOSE))
    # await asyncio.sleep(3)
    await callback.message.answer(MessageTexts.CHOOSE_SECTION.value,
                                  reply_markup=await keyboard_builder(1, *[button.value for button in
                                                                           TestingSections],
                                                                      BasicButtons.MAIN_MENU))
    await state.set_state(TestingFSM.selecting_section)


@user_testing_router.callback_query((F.data == 'choose_other_section_training'))
async def start_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отличный выбор!')
    await callback.message.edit_text(MessageTexts.CHOOSE_SECTION.value,
                                     reply_markup=await keyboard_builder(1, *[button.value for button in
                                                                              TestingSections],
                                                                         BasicButtons.MAIN_MENU))
    await state.set_state(TestingFSM.selecting_section)


@user_testing_router.callback_query((F.data == BasicButtons.BACK.value),
                                    StateFilter(TestingFSM.selecting_subsection))
async def start_testing(callback: CallbackQuery, state: FSMContext):  # выбор раздела для прохождения тесте
    await callback.answer()
    await callback.message.edit_text(MessageTexts.CHOOSE_SECTION.value,
                                     reply_markup=await keyboard_builder(1, *[button.value for button in
                                                                              TestingSections],
                                                                         BasicButtons.MAIN_MENU))
    await state.set_state(TestingFSM.selecting_section)


@user_testing_router.callback_query(
    StateFilter(TestingFSM.selecting_section))  # выбор подраздела для прохождения теста
async def choosing_section_testing(callback: CallbackQuery, state: FSMContext):
    section = testing_section_mapping.get(callback.data)
    await callback.answer()
    if section is None:
        await callback.message.edit_text(MessageTexts.ERROR.value)
        await state.set_state(TestingFSM.default)
        return

    await callback.message.edit_text(
        MessageTexts.CHOOSE_SUBSECTION_TEST.value,
        reply_markup=await keyboard_builder(1, *[button.value for button in section], BasicButtons.BACK,
                                            BasicButtons.MAIN_MENU))
    await state.set_state(TestingFSM.selecting_subsection)
    await update_state_data(state, section=callback.data, subsection=None)


@user_testing_router.callback_query(
    StateFilter(TestingFSM.selecting_subsection))  # подраздел выбран, получен в callback
async def choosing_subsection_testing(callback: CallbackQuery, state: FSMContext):
    subsection = callback.data
    data = await state.get_data()
    section = data.get('section')
    count_exercises = await exercise_manager.get_count_testing_exercises_in_subsection(section=section,
                                                                                       subsection=subsection)
    await callback.answer()
    if count_exercises > 0:
        await callback.message.edit_text(f"""Ты выбрал:\n «{section} - {subsection}»\n
Готов проходить?""", reply_markup=await keyboard_builder(1, BasicButtons.MAIN_MENU, args_go_first=False,
                                                         ready_for_test=BasicButtons.READY))
        await update_state_data(state, subsection=subsection)
        await state.set_state(TestingFSM.selected_subsection)
    elif count_exercises == 0:
        await callback.message.edit_text(
            MessageTexts.EMPTY_SECTION.value,
            reply_markup=await keyboard_builder(1,
                                                choose_other_section_training=BasicButtons.CHOOSE_OTHER_SECTION))


@user_testing_router.callback_query((F.data == 'ready_for_test'))
async def chose_subsection_testing(callback: CallbackQuery, state: FSMContext, prev_message_delete: bool = True):
    await callback.answer()
    if prev_message_delete:
        await callback.message.delete()
    else:
        pass
    data = await state.get_data()
    subsection, section, user_id = data.get('subsection'), data.get('section'), callback.from_user.id
    exercise = await exercise_manager.get_random_testing_exercise(section=section, subsection=subsection,
                                                                  user_id=user_id)

    if exercise:
        test, answer, id_exercise = exercise
    else:
        first_try_count, success_count, total_exercises_count = await user_progress_manager.get_counts_completed_exercises_testing(
            user_id=user_id, section=section,
            subsection=subsection)
        await callback.message.answer(f"""{MessageTexts.ALL_EXERCISES_COMPLETED.value}
Всего заданий выполнено: <b>{success_count} из {total_exercises_count}</b>
С первой попытки: <b>{first_try_count}</b>""",
                                      reply_markup=await keyboard_builder(1,
                                                                          choose_other_section_training=BasicButtons.CHOOSE_OTHER_SECTION,
                                                                          start_again_test=BasicButtons.START_AGAIN))
        return
    await callback.message.answer(test)
    await state.set_state(TestingFSM.in_process)
    await update_state_data(state, current_test=test, current_answer=answer.strip(), current_id=id_exercise)


@user_testing_router.message(StateFilter(TestingFSM.in_process))  # В процессе тестирования
async def in_process_testing(message: Message, state: FSMContext):
    data = await state.get_data()
    section, subsection, exercise_id, user_id = data.get('section'), data.get('subsection'), data.get(
        'current_id'), message.from_user.id
    answer = data.get('current_answer')
    if message.text.lower() == answer.lower():
        first_try = await user_progress_manager.mark_exercise_completed(exercise_type='Testing',
                                                                        section=section,
                                                                        subsection=subsection,
                                                                        exercise_id=exercise_id, user_id=user_id,
                                                                        success=True)
        data = await state.get_data()
        subsection, section, user_id = data.get('subsection'), data.get('section'), message.from_user.id
        exercise = await exercise_manager.get_random_testing_exercise(section=section,
                                                                      subsection=subsection,
                                                                      user_id=user_id)

        if not exercise:
            first_try_count, success_count, total_exercises_count = await user_progress_manager.get_counts_completed_exercises_testing(
                user_id=user_id, section=section,
                subsection=subsection)
            await message.answer(f"""{MessageTexts.ALL_EXERCISES_COMPLETED.value}
Всего заданий выполнено: <b>{success_count} из {total_exercises_count}</b>
С первой попытки: <b>{first_try_count}</b>""",
                                 reply_markup=await keyboard_builder(1, start_again_test=BasicButtons.START_AGAIN,
                                                                     choose_other_section_training=BasicButtons.CHOOSE_OTHER_SECTION))
            await send_message_to_admin(message.bot, text=f"""Пользователь @{message.from_user.username} выполнил тест
<b>{section} – {subsection}</b>\nС первой попытки <b>{first_try_count} из {success_count}</b>""")
        else:
            test, answer, id_exercise = exercise
            await update_state_data(state, current_test=test, current_answer=answer.strip(), current_id=id_exercise)
            if first_try:
                await message.answer(f'{random.choice(list_right_answers)}\nYou got it on the first try!')
                await message.answer(test)
            else:
                await message.answer(f'{random.choice(list_right_answers)}')
                await message.answer(test)

    else:
        await message.answer(MessageTexts.INCORRECT_ANSWER.value,
                             reply_markup=await keyboard_builder(1, see_answer_testing=BasicButtons.SEE_ANSWER))
        await user_progress_manager.mark_exercise_completed(exercise_type='Testing', section=section,
                                                            subsection=subsection,
                                                            exercise_id=exercise_id, user_id=user_id, success=False)


@user_testing_router.callback_query((F.data == 'start_again_test'))
async def start_again_testing(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(MessageTexts.ARE_YOU_SURE_START_AGAIN.value,
                                     reply_markup=await keyboard_builder(1, BasicButtons.CLOSE, args_go_first=False,
                                                                         sure_start_again_test=BasicButtons.START_AGAIN))


@user_testing_router.callback_query((F.data == 'sure_start_again_test'))
async def start_again_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    subsection, section, user_id = data.get('subsection'), data.get('section'), callback.from_user.id
    await user_progress_manager.delete_progress_by_subsection(user_id=user_id, section=section, subsection=subsection)
    await callback.message.edit_text(f'Прогресс по тесту {section} – {subsection} сброшен')
    await chose_subsection_testing(callback, state, prev_message_delete=False)


@user_testing_router.callback_query((F.data == 'see_answer_testing'))  # Подсказка в тестировании
async def see_answer_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    answer = data.get('current_answer')
    await callback.message.edit_text(f'Правильный ответ: {answer.capitalize()}')
    await asyncio.sleep(3)
    await chose_subsection_testing(callback, state, prev_message_delete=False)
