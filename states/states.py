from aiogram.filters.state import State, StatesGroup


class LearningFSM(StatesGroup):
    default = State()
    choose_type_of_exercise = State()
    testing = State()  # Пользователь проходит тренажер по грамматике
    testing_choosing_section = State()  # Пользователь выбирает раздел в тренажере по грамматике
    testing_choosed_section = State()  # Пользователь выбрал раздел в тренажере по грамматике

    verbs_learning = State()  # Пользователь изучает неправильные глаголы
    new_words_learning = State()  # Пользователь изучает новые слова
    existing_user = State()  # Состояние для существующих пользователей (без приветственного сообщения)


class AdminFSM(StatesGroup):
    default = State()  # Начальное состояние
    choose_section_testing = State()
    choose_subsection_testing = State()
    choose_management_action_testing = State()
    adding_exercise_testing = State()
    deleting_exercise_testing = State()
    editing_exercise_testing = State()

    manage_users = State()  # Управление пользователями
    view_reports = State()  # Просмотр отчетов
    configure_settings = State()  # Настройка параметров
