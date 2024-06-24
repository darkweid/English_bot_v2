from aiogram import Router, F
from config_data.config import Config, load_config
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from states import AdminFSM, LearningFSM
from db import ExerciseManager, UserProgressManager, UserManager
from keyboards import *
from lexicon import *
from utils import message_to_admin, update_state_data

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
ADMINS: list = config.tg_bot.admin_ids

admin_router: Router = Router()
exercise_manager: ExerciseManager = ExerciseManager()
user_progress_manager: UserProgressManager = UserProgressManager()
user_manager: UserManager = UserManager()


@admin_router.message(Command(commands=["test"]))
async def admin_command(message: Message, state: FSMContext):
    for user in (await user_manager.get_all_users()):
        await message.answer(str(user))
    await user_progress_manager.get_completed_exercises_testing(user_id=message.from_user.id, section='Tenses',
                                                                subsection='Present Simple')


@admin_router.message(Command(commands=["admin"]))
async def admin_command(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer('🔘 Привет, что будем делать? 🔘',
                             reply_markup=await keyboard_builder(1, AdminMenuButtons.EXERCISES,
                                                                 AdminMenuButtons.SEE_ACTIVITY_DAY,
                                                                 AdminMenuButtons.SEE_ACTIVITY_WEEK,
                                                                 AdminMenuButtons.SEE_ACTIVITY_MONTH,
                                                                 AdminMenuButtons.USERS, AdminMenuButtons.EXIT))
        await state.set_state(AdminFSM.default)
    else:
        await message.answer('🚫 Вам сюда нельзя 🚫')


@admin_router.callback_query((F.data == AdminMenuButtons.MAIN_MENU.value))
async def admin_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('🔘 Привет, что будем делать? 🔘',
                                     reply_markup=await keyboard_builder(1, AdminMenuButtons.EXERCISES,
                                                                         AdminMenuButtons.SEE_ACTIVITY_DAY,
                                                                         AdminMenuButtons.SEE_ACTIVITY_WEEK,
                                                                         AdminMenuButtons.SEE_ACTIVITY_MONTH,
                                                                         AdminMenuButtons.USERS, AdminMenuButtons.EXIT))
    await state.set_state(AdminFSM.default)


@admin_router.callback_query((F.data == 'close_message_admin'), ~StateFilter(AdminFSM.see_user_info))
@admin_router.callback_query((F.data == AdminMenuButtons.EXIT.value))
async def admin_exit(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer('До скорых встреч 👋')
    await update_state_data(state, admin_section=None, admin_subsection=None, index_testing_edit=None,
                            index_testing_delete=None)
    await state.set_state(LearningFSM.default)


@admin_router.callback_query((F.data == 'stats_users_table_close'))  # close without change state
async def close_message_without_state_changes(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()


@admin_router.callback_query((F.data == AdminMenuButtons.EXERCISES.value), StateFilter(AdminFSM.default))
@admin_router.callback_query((F.data == BasicButtons.BACK.value), StateFilter(AdminFSM.choose_section_testing))
async def admin_exercises(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выбери группу упражнений:',
                                     reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU,
                                                                         AdminMenuButtons.EXIT,
                                                                         args_go_first=False,
                                                                         tests_admin=AdminMenuButtons.TESTING,
                                                                         new_words_admin=AdminMenuButtons.NEW_WORDS,
                                                                         irr_verbs_admin=AdminMenuButtons.IRR_VERBS))


@admin_router.callback_query((F.data == BasicButtons.BACK.value), StateFilter(AdminFSM.choose_subsection_testing))
@admin_router.callback_query((F.data == 'tests_admin'))
async def admin_start_testing(callback: CallbackQuery, state: FSMContext):  # выбор раздела для прохождения тесте
    await callback.answer()
    await callback.message.edit_text('Выбери раздел тестов:', reply_markup=choose_section_testing_keyboard)
    await state.set_state(AdminFSM.choose_section_testing)


@admin_router.callback_query(StateFilter(AdminFSM.choose_section_testing))  # выбор ПОДраздела теста
async def admin_choosing_section_testing(callback: CallbackQuery, state: FSMContext):
    section = testing_section_mapping.get(callback.data)
    if section is None:
        await callback.answer()
        await callback.message.edit_text(MessageTexts.ERROR)
        await state.set_state(LearningFSM.default)
        return

    await callback.message.edit_text(
        MessageTexts.CHOOSE_SUBSECTION_TEST.value,
        reply_markup=await keyboard_builder(1, *[button.value for button in section], BasicButtons.BACK,
                                            BasicButtons.MAIN_MENU))
    await state.set_state(AdminFSM.choose_subsection_testing)
    await update_state_data(state, admin_section=callback.data, admin_subsection=None)
    print(await state.get_data())


@admin_router.callback_query(
    StateFilter(AdminFSM.choose_subsection_testing))  # подраздел выбран, получен в callback
async def admin_choosing_subsection_testing(callback: CallbackQuery, state: FSMContext):
    admin_subsection = callback.data
    data = await state.get_data()
    admin_section = data.get('admin_section')
    await callback.answer()
    await callback.message.edit_text(
        f'Выбран раздел\n «{admin_section} - {admin_subsection}»\n\nЧто нужно сделать?',
        reply_markup=await keyboard_builder(1, AdminMenuButtons.SEE_EXERCISES_TESTING,
                                            AdminMenuButtons.ADD_EXERCISE_TESTING,
                                            AdminMenuButtons.EDIT_EXERCISE_TESTING,
                                            AdminMenuButtons.DEL_EXERCISE_TESTING,
                                            AdminMenuButtons.MAIN_MENU,
                                            AdminMenuButtons.EXIT))
    await update_state_data(state, admin_subsection=admin_subsection)
    print(await state.get_data())
    await state.set_state(AdminFSM.choose_management_action_testing)


@admin_router.callback_query(F.data == AdminMenuButtons.SEE_EXERCISES_TESTING.value)
@admin_router.callback_query(F.data == AdminMenuButtons.ADD_EXERCISE_TESTING.value)
@admin_router.callback_query(F.data == AdminMenuButtons.EDIT_EXERCISE_TESTING.value)
@admin_router.callback_query(F.data == AdminMenuButtons.DEL_EXERCISE_TESTING.value)
async def admin_testing_management(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subsection, section = data.get('admin_subsection'), data.get('admin_section')
    exercise_name = f'\"{section} - {subsection}\"'

    if section and callback.data == AdminMenuButtons.SEE_EXERCISES_TESTING.value:
        result = await exercise_manager.get_testing_exercises(subsection)
        if result:
            await callback.answer()
            await send_long_message(callback, f'Вот все предложения из раздела\n{exercise_name}:\n{result}',
                                    reply_markup=await keyboard_builder(1, close_message_admin=AdminMenuButtons.CLOSE))
        else:
            await callback.answer()
            await callback.message.edit_text(f'В разделе \n{exercise_name} ещё нет упражнений',
                                             reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU,
                                                                                 AdminMenuButtons.EXIT))


    elif callback.data == AdminMenuButtons.ADD_EXERCISE_TESTING.value:
        await callback.message.edit_text(f"""Введи предложение и ответ к нему для добавления в раздел\n{exercise_name}\n
В формате: \nEnglish sentence=+=Answer
\nМожно отправить несколько упражнений, тогда каждое упражнение должно начинаться с новой строки
и сообщение должно содержать не более 4096 символов(лимит Telegram)""",
                                         reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU,
                                                                             AdminMenuButtons.EXIT))
        await state.set_state(AdminFSM.adding_exercise_testing)

    elif callback.data == AdminMenuButtons.EDIT_EXERCISE_TESTING.value:
        await callback.message.edit_text(f'Введи номер предложения для редактирования в разделе\n{exercise_name}\n',
                                         reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU,
                                                                             AdminMenuButtons.EXIT))
        await state.set_state(AdminFSM.editing_exercise_testing)


    elif callback.data == AdminMenuButtons.DEL_EXERCISE_TESTING.value:
        await callback.message.edit_text(f"""Введи номер предложения для удаления из\n{exercise_name}\n
Если нужно удалить одно предложение - введи номер предложения, если несколько - введи номера предложений через запятую""",
                                         reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU,
                                                                             AdminMenuButtons.EXIT))
        await state.set_state(AdminFSM.deleting_exercise_testing)


@admin_router.message(StateFilter(AdminFSM.adding_exercise_testing))  # ADD
async def admin_adding_sentence_grammar(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        subsection, section = data.get('admin_subsection'), data.get('admin_section')
        sentences = message.text.split('\n')
        count_sentences = len(sentences)
        if count_sentences > 1:
            for group_sentences in sentences:
                test, answer = group_sentences.split('=+=')
                await exercise_manager.add_testing_exercise(section=section, subsection=subsection, test=test,
                                                            answer=answer)
            await message.answer(
                f'✅Успешно добавлено {count_sentences} упражнений, можешь отправить ещё',
                reply_markup=await keyboard_builder(1, AdminMenuButtons.EXIT))

        else:
            test, answer = message.text.split('=+=')
            await exercise_manager.add_testing_exercise(section=section, subsection=subsection, test=test,
                                                        answer=answer)

            await message.answer('✅Упражнение успешно добавлено, можешь отправить ещё и я добавлю',
                                 reply_markup=await keyboard_builder(1, AdminMenuButtons.EXIT))

    except Exception as e:
        print('\n\n\n\n' + str(e) + '\n\n\n\n')
        await message.answer('❗️Что-то пошло не так, попробуй еще раз\n\nПроверь формат текста',
                             reply_markup=await keyboard_builder(1, AdminMenuButtons.EXIT))
        await message.answer(str(e))


@admin_router.message(StateFilter(AdminFSM.editing_exercise_testing))  # EDIT
async def admin_editing_sentence_grammar(message: Message, state: FSMContext):
    if message.text.isdigit():
        index = int(message.text)
        await update_state_data(state, index_testing_edit=index)
        data = await state.get_data()
        subsection, section, index_testing_edit = data.get('admin_subsection'), data.get('admin_section'), data.get(
            'index_testing_edit')
        exercise_name = f'\"{section} - {subsection}\"'
        await message.answer(f"""Отлично, будем изменять \nпредложение № {index_testing_edit}\nВ разделе {exercise_name} 
Введи предложение и ответ к нему в формате: \nEnglish sentence=+=Answer""")
        await state.set_state(AdminFSM.ready_to_edit_exercise_testing)
    else:
        await message.answer('❌Что-то пошло не так, попробуй еще раз',
                             reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU, AdminMenuButtons.EXIT))


@admin_router.message(StateFilter(AdminFSM.ready_to_edit_exercise_testing))  # EDIT
async def admin_edit_sentence_grammar(message: Message, state: FSMContext):
    data = await state.get_data()
    subsection, section, index_testing_edit = data.get('admin_subsection'), data.get('admin_section'), data.get(
        'index_testing_edit')
    try:
        test, answer = message.text.split('=+=')
        await exercise_manager.edit_testing_exercise(section=section, subsection=subsection, test=test, answer=answer,
                                                     index=index_testing_edit)
        await message.answer('✅Успешно изменено',
                             reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU))
        await state.set_state(AdminFSM.default)
        await update_state_data(state, admin_section=None, admin_subsection=None, index_testing_edit=None)
    except Exception as e:
        await message.answer('❌Что-то пошло не так, попробуй еще раз',
                             reply_markup=await keyboard_builder(1, AdminMenuButtons.EXIT))
        print('\n\n\n\n', e, '\n\n\n\n')


@admin_router.message(StateFilter(AdminFSM.deleting_exercise_testing))  # DELETE
async def admin_deleting_sentence_grammar(message: Message, state: FSMContext):
    data = await state.get_data()
    subsection, section = data.get('admin_subsection'), data.get('admin_section')
    exercise_name = f'\"{section} - {subsection}\"'
    indexes = []
    try:
        indexes = [int(num) for num in message.text.split(',')]
    except ValueError:
        await message.answer('❌Неправильный формат, попробуй еще раз ввести номер предложения',
                             reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU, AdminMenuButtons.EXIT))

    if len(indexes) == 1:
        index = indexes[0]
        await message.answer(f"""✅Предложение № {index}\n<b>Удалено</b> из раздела \n{exercise_name}""",
                             reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU, AdminMenuButtons.EXIT))
        await exercise_manager.delete_testing_exercise(section=section, subsection=subsection, index=index)
    elif len(indexes) > 1:
        await message.answer(f"""✅Предложения № {str(indexes)}\n <b>Удалены</b> из раздела \n{exercise_name}""",
                             reply_markup=await keyboard_builder(1, AdminMenuButtons.MAIN_MENU, AdminMenuButtons.EXIT))
        for index in indexes:
            await exercise_manager.delete_testing_exercise(section=section, subsection=subsection, index=index)


# Users

@admin_router.callback_query(F.data == AdminMenuButtons.USERS.value)
async def admin_users(callback: CallbackQuery, state: FSMContext):
    users = await user_manager.get_all_users()
    users_ranks_and_points = await user_progress_manager.get_all_users_ranks_and_points(medals_rank=True)
    rank_info = f"""<pre>Рейтинг всех пользователей:\n
[{'№'.center(6)}] [{'Баллы'.center(7)}] [{'Имя'.center(20)}]\n"""
    count = 0
    for user in users_ranks_and_points:
        if count < 3:
            rank_info += f"[{user.get('rank').center(5)}] [{user.get('points').center(7)}] [{user.get('full_name').center(20)}]\n"
        else:
            rank_info += f"[{user.get('rank').center(6)}] [{user.get('points').center(7)}] [{user.get('full_name').center(20)}]\n"
        count += 1
    rank_info += "</pre>"

    await callback.message.answer(rank_info,
                                  reply_markup=await keyboard_builder(1,
                                                                      stats_users_table_close=AdminMenuButtons.CLOSE))
    await callback.message.answer('Нажми на кнопку для получения информации о пользователе:',
                                  reply_markup=await keyboard_builder_users(users))
    await state.set_state(AdminFSM.see_user_info)


@admin_router.callback_query(F.data == AdminMenuButtons.CLOSE.value, StateFilter(AdminFSM.see_user_info))
async def admin_see_user_info_close_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()


@admin_router.callback_query(StateFilter(AdminFSM.see_user_info))
async def admin_see_user_info(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data)
    info = await user_manager.get_user_info_text(user_id)
    await callback.message.answer(info, reply_markup=await keyboard_builder(1, AdminMenuButtons.CLOSE))


@admin_router.callback_query(F.data == AdminMenuButtons.SEE_ACTIVITY_DAY.value)
@admin_router.callback_query(F.data == AdminMenuButtons.SEE_ACTIVITY_WEEK.value)
@admin_router.callback_query(F.data == AdminMenuButtons.SEE_ACTIVITY_MONTH.value)
async def admin_activity(callback: CallbackQuery, state: FSMContext):
    cbdata = callback.data
    if cbdata == AdminMenuButtons.SEE_ACTIVITY_DAY.value:
        interval = 0
    elif cbdata == AdminMenuButtons.SEE_ACTIVITY_WEEK.value:
        interval = 7
    elif cbdata == AdminMenuButtons.SEE_ACTIVITY_MONTH.value:
        interval = 30
    info = await user_progress_manager.get_activity(interval)
    await callback.message.answer(info,
                                  reply_markup=await keyboard_builder(1, close_message_admin=AdminMenuButtons.CLOSE))


async def send_long_message(callback, text, max_length=4000, **kwargs):
    paragraphs = text.split('\n')
    current_message = ""

    for paragraph in paragraphs:
        if len(current_message) + len(paragraph) < max_length:
            current_message += paragraph + '\n'
        else:
            await callback.message.answer(current_message, **kwargs)
            current_message = paragraph + '\n'
    print(len(current_message))
    if current_message:
        await callback.message.answer(current_message, **kwargs)
