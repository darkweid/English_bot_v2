from aiogram.filters.state import State, StatesGroup

class TestFSM(StatesGroup):
    test = State()

class LearningFSM(StatesGroup):
    default = State()
    choose_type_of_exercise = State()
    grammar_training = State() # Пользователь проходит тренажер по грамматике
    grammar_choosing_section = State()# Пользователь выбирает раздел в тренажере по грамматике
    grammar_choosed_section = State()# Пользователь выбрал раздел в тренажере по грамматике

    verbs_learning = State()  # Пользователь изучает неправильные глаголы
    new_words_learning = State()  # Пользователь изучает новые слова
    existing_user = State()  # Состояние для существующих пользователей (без приветственного сообщения)


class AdminFSM(StatesGroup):
    default = State()  # Начальное состояние
    choose_type_of_exercise_grammar = State()
    choose_what_to_do_with_exercise_grammar = State()
    adding_sentence_grammar = State()
    deleting_exercise_grammar = State()
    manage_users = State()  # Управление пользователями
    view_reports = State()  # Просмотр отчетов
    configure_settings = State()  # Настройка параметров
