from aiogram.filters.state import State, StatesGroup


class LearningFSM(StatesGroup):
    grammar_training = State()  # Пользователь проходит тренажер по грамматике
    verbs_learning = State()  # Пользователь изучает неправильные глаголы
    new_words_learning = State()  # Пользователь изучает новые слова
    existing_user = State()  # Состояние для существующих пользователей (без приветственного сообщения)


class AdminFSM(StatesGroup):
    default = State()  # Начальное состояние
    manage_users = State()  # Управление пользователями
    view_reports = State()  # Просмотр отчетов
    configure_settings = State()  # Настройка параметров
