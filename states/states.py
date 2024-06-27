from aiogram.filters.state import State, StatesGroup


class LearningFSM(StatesGroup):
    default = State()
    choose_type_of_exercise = State()
    testing = State()  # Пользователь проходит тестирование
    testing_choosing_section = State()  # Пользователь выбирает раздел в тестах
    testing_choosing_subsection = State()  # Пользователь выбирает подраздел в тестах
    testing_choosed_subsection = State()    # Пользователь выбрал подраздел в тестах
    testing_in_process = State()

    verbs_learning = State()  # Пользователь изучает неправильные глаголы
    new_words_learning = State()  # Пользователь изучает новые слова
    existing_user = State()# Состояние для существующих пользователей (без приветственного сообщения)
    set_reminder_time = State()


class AdminFSM(StatesGroup):
    default = State()  # Начальное состояние

    choose_section_testing = State()
    choose_subsection_testing = State()
    choose_management_action_testing = State()
    adding_exercise_testing = State()
    deleting_exercise_testing = State()
    editing_exercise_testing = State()
    ready_to_edit_exercise_testing = State()
    ready_to_delete_exercise_testing = State()

    see_user_info = State()

    broadcasting_set_date_time = State()
    broadcasting_set_text = State()


