import asyncio, random

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states import WordsLearningFSM
from utils import send_message_to_admin, update_state_data, send_long_message
from lexicon import *
from db import *
from keyboards import *

user_new_words_router: Router = Router()
user_manager: UserManager = UserManager()
user_words_manager = UserWordsLearningManager()
words_manager = NewWordsExerciseManager()
daily_stats_manager = DailyStatisticsManager()


@user_new_words_router.callback_query(F.data == MainMenuButtons.NEW_WORDS.value)
async def start_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text('Выбирай:',
                                     reply_markup=await keyboard_builder(1, BasicButtons.MAIN_MENU, args_go_first=False,
                                                                         learn_new_words=BasicButtons.LEARN_ADDED_WORDS,
                                                                         add_new_words=BasicButtons.ADD_WORDS,
                                                                         progress_new_words=BasicButtons.NEW_WORDS_PROGRESS))
    await state.set_state(WordsLearningFSM.default)


@user_new_words_router.callback_query(F.data == 'back_to_main_menu_new_words')
async def start_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Выбирай:',
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
async def learn_new_words(callback: CallbackQuery, state: FSMContext, hello_message: bool = True):
    await callback.answer()
    user_id = callback.from_user.id
    exercise = await user_words_manager.get_random_word_exercise(user_id=user_id)
    count_user_exercise = await user_words_manager.get_count_active_learning_exercises(user_id=user_id)
    count_user_exercises_for_today = await user_words_manager.get_count_all_exercises_for_today_by_user(user_id=user_id)
    learned_words = await user_words_manager.get_count_learned_exercises(user_id=user_id)

    if not exercise:
        await callback.message.answer(f"""{random.choice(list_right_answers)}🔥
{MessageTexts.NO_WORDS_TO_LEARN_TODAY.value}
Cлов/идиом в активном изучении: {count_user_exercise}
Изучено всего: {learned_words}""",
                                      reply_markup=await keyboard_builder(1, BasicButtons.MAIN_MENU,
                                                                          BasicButtons.CLOSE))
    else:
        if hello_message:
            await callback.message.edit_text(f"""{MessageTexts.NEW_WORDS_HELLO.value}
Cлов в активном изучении: {count_user_exercise}
Для изучения сегодня: {count_user_exercises_for_today}
Изучено всего: {learned_words}""",
                                             reply_markup=await keyboard_builder(1, rules_new_words=BasicButtons.RULES,
                                                                                 close_rules_new_words=BasicButtons.CLOSE))

        word_russian, word_english, word_id, options = exercise['russian'], exercise['english'], exercise[
            'exercise_id'], exercise['options']
        await update_state_data(state, words_section=exercise['section'], words_subsection=exercise['subsection'],
                                words_exercise_id=exercise['exercise_id'], test=word_russian, answer=word_english)

        await callback.message.answer(word_russian.capitalize(),
                                      reply_markup=await keyboard_builder_words_learning(1, correct=word_english,
                                                                                         options=options))
        await state.set_state(WordsLearningFSM.in_process)


@user_new_words_router.callback_query(F.data == 'correct',
                                      StateFilter(WordsLearningFSM.in_process))
async def correct_answer_learning_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(f'🔥🔥🔥{random.choice(list_right_answers)}')
    await asyncio.sleep(0.7)
    await callback.message.delete()
    user_id = callback.from_user.id
    data = await state.get_data()
    section, subsection, exercise_id = data.get('words_section'), data.get('words_subsection'), data.get(
        'words_exercise_id')
    await user_words_manager.set_progress(user_id=user_id, section=section, subsection=subsection,
                                          exercise_id=exercise_id, success=True)

    await learn_new_words(callback, state, hello_message=False)
    await daily_stats_manager.update('new_words')


@user_new_words_router.callback_query(F.data == 'not_correct',
                                      StateFilter(WordsLearningFSM.in_process))
async def not_correct_answer_learning_words(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    test, answer = user_data.get('test'), user_data.get('answer')

    await callback.message.edit_text(f'😕\n{test} — {answer}')
    await asyncio.sleep(1)
    await callback.message.edit_text(f'{test} — {answer}')
    await asyncio.sleep(0.2)
    data = await state.get_data()
    user_id = callback.from_user.id
    section, subsection, exercise_id = data.get('words_section'), data.get('words_subsection'), data.get(
        'words_exercise_id')
    await user_words_manager.set_progress(user_id=user_id, section=section, subsection=subsection,
                                          exercise_id=exercise_id, success=False)
    await learn_new_words(callback, state, hello_message=False)
    await daily_stats_manager.update('new_words')


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
    section = callback.data
    user_id = callback.from_user.id
    user_added_subsections = await user_words_manager.get_added_subsections_by_user(user_id=user_id)
    subsections = await words_manager.get_subsection_names(section=section)
    buttons = [subsection for subsection in subsections if subsection not in user_added_subsections]
    if len(buttons) > 0:
        await callback.answer()
        await callback.message.edit_text(
            MessageTexts.SELECT_SUBSECTION_WORDS.value,
            reply_markup=await keyboard_builder(1, *buttons,  # subsection buttons
                                                back_to_sections=BasicButtons.BACK,
                                                back_to_main_menu_new_words=BasicButtons.MAIN_MENU_NEW_WORDS))
        await state.set_state(WordsLearningFSM.selecting_subsection)
        await update_state_data(state, section=section, subsection=None)
    elif len(buttons) == 0:
        await callback.answer('В этом разделе больше нет тем для добавления 🧐')


@user_new_words_router.callback_query(StateFilter(WordsLearningFSM.selecting_subsection))
async def add_new_words_selecting_subsection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    section = user_data.get('section')
    subsection = callback.data
    quantity = await words_manager.get_count_new_words_exercises_in_subsection(section=section, subsection=subsection)
    word_declension = await get_word_declension(quantity)
    await callback.message.edit_text(f"""{subsection} – {section}
В теме {word_declension}
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
    user_data = await state.get_data()
    section, subsection, user_id = user_data.get('section'), user_data.get('subsection'), callback.from_user.id
    user_answer = callback.data
    if user_answer == 'add_words':
        await user_words_manager.add_words_to_learning(section=section, subsection=subsection, user_id=user_id)
        await callback.message.edit_text(
            'Добавлено',
            reply_markup=await keyboard_builder(1,
                                                back_to_main_menu_new_words=BasicButtons.MAIN_MENU_NEW_WORDS))
        await send_message_to_admin(text=f"""Пользователь @{callback.from_user.username} добавил
тему «{section} – {subsection}» в изучение""")
    elif user_answer == 'do_not_add_words':
        await callback.message.edit_text(
            'Слова не добавлены',
            reply_markup=await keyboard_builder(1,
                                                back_to_main_menu_new_words=BasicButtons.MAIN_MENU_NEW_WORDS))
        await update_state_data(state, section=None, subsection=None)


@user_new_words_router.callback_query(F.data == 'progress_new_words')
async def stats_new_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    stats = await user_words_manager.get_user_stats(user_id=user_id)
    stats_text = ''
    for subsection, data in stats.items():
        if subsection.isdigit():
            subsection = 'Personal Words'
        learned = data['learned']
        for_today_learning = data['for_today_learning']
        total_words_in_subsection = data['total_words_in_subsection']
        active_learning = data['active_learning']
        success_rate = data['success_rate']
        stats_text += (f'Тема <b>«{subsection}»</b>\n'
                       f'Для изучения сегодня: {for_today_learning}\n'
                       f'Всего слов в теме: {total_words_in_subsection}\n'
                       f'В активном изучении: {active_learning}\n'
                       f'Изучено: {learned}\n'
                       f'Правильных ответов: {success_rate:.0f}%\n\n')
    if len(stats_text) == 0:
        await callback.message.edit_text('У тебя еще нет статистики в изучении слов',
                                         reply_markup=await keyboard_builder(1,
                                                                             back_to_main_menu_new_words=BasicButtons.BACK))
    elif len(stats_text) > 4000:
        await send_long_message(callback=callback, text=stats_text, delimiter='\n\n',
                                reply_markup=await keyboard_builder(1, close_message=BasicButtons.CLOSE))
    else:
        await callback.message.edit_text(stats_text,
                                         reply_markup=await keyboard_builder(1,
                                                                             back_to_main_menu_new_words=BasicButtons.BACK))


async def get_word_declension(count: int) -> str:
    if count % 10 == 1 and count % 100 != 11:
        return f"{count} слово"
    elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
        return f"{count} слова"
    else:
        return f"{count} слов"
