from enum import Enum


class MessageTexts(Enum):
    WELCOME_NEW_USER = f"""Помогаю людям изучать английский.
У меня три раздела:
– тренажер по грамматике
- запоминание неправильных глаголов
– запоминание новых слов

Так же ты можешь выбрать удобное тебе время по кнопке ниже, а я буду напоминать заниматься😉
Если хочешь - можешь установить время напоминаний позже из меню слева """
    WELCOME_EXISTING_USER = '🔻 Чем займёмся сегодня? 🔻'
    GIVE_A_HINT = '<u>Попробуй ещё раз</u> или попроси меня показать ответ 😉'
    LETS_CONTINUE = 'Продолжаем 😊'
    LEARN_FROM_MISTAKES = 'На ошибках учатся, так что продолжаем 😊'
    TESTING_HELLO = 'Хороший выбор!\nБудем улучшать твою <b>грамматику</b>\nЕсли нужно - жми кнопку ниже и посмотри правила'
    INFO_RULES = f"""\n🟢Весь прогресс сохраняется в памяти бота
\n🔵Регистр введенных предложений/слов не имеет значения.
\n❌Не используй сокращения «don't», «it's»
✅Используй полные формы «do not», «it is»
\n🟠В любой непонятной ситуации нажимай команду /start и бот перезапустится 😊"""
    ERROR = 'Что-то пошло не так😐\nПерезапусти бота, нажми команду /start'
    TEST_RULES = """Правила простые:\nЯ пишу предложение на английском с пробелом, а ты должен мне написать, что нужно добавить в этот пробел\n\nЕсли ответы не совпадут:
⚪ Можешь попробовать написать ответ ещё раз(количество попыток не ограничено)\n⚪ Можешь поcмотреть ответ, нажав на кнопку «Покажи ответ»"""
    CHOOSE_SECTION =         'Выбери раздел для прохождения теста:'
    CHOOSE_SUBSECTION_TEST = 'Выбери тему для прохождения теста:'
    ALL_EXERCISES_COMPLETED = 'Все упражнения в этом разделе выполнены🎉\nНо ты можешь выбрать другой раздел'
    INCORRECT_ANSWER = '❌ Хм, у меня другой ответ 🤔\n\n<b>Попробуй ещё раз</b> или попроси меня показать ответ 😉'
    GIVE_ME_YOUR_ANSWER = 'Напиши мне чем заполнить пробел в предложении:'


class MainMenuButtons(Enum):
    TESTING = 'Тесты'
    IRREGULAR_VERBS = 'Изучение неправильных глаголов'
    NEW_WORDS = 'Изучение новых слов'
    TRANSLATING_SENTENCES = 'Предложения для перевода'


class BasicButtons(Enum):
    YES = '✅ <b>ДА!</b>'
    NO = '❌ <b>НЕТ</b>'
    READY = 'Готов!'
    BACK = '⬅️Назад'
    SET = 'Установить'
    CHOOSE_OTHER_SECTION = 'Выбрать другую тему'
    MAIN_MENU = '🏠Главное меню'
    CANCEL = 'Отменить'
    CLOSE = 'Закрыть'
    RULES = '🙋‍♀️ Посмотреть правила 🙋'
    SEE_ANSWER = '🔎 Показать ответ 🔍'
    REMINDER_TIME = 'Установить время напоминаний'


class TestingSections(Enum):
    TENSES = 'Tenses'
    CONSTRUCTIONS = 'Constructions'
    PHRASES_AND_WORDS = 'Phrases & words'
    PREPOSITIONS = 'Prepositions'
    MODAL_VERBS = 'Modal verbs'
    CONDITIONALS = 'Conditionals'


class TensesSections(Enum):
    PRESENT_SIMPLE = 'Present Simple'
    PRESENT_CONTINUOUS = 'Present Continuous'
    PS_VS_PC = 'Present Simple VS Present Continuous'
    PAST_SIMPLE = 'Past Simple'
    PAST_SIMPLE_WITH_IRR_VERBS = 'Past Simple with irregular verbs'
    PRESENT_PERFECT_SIMPLE = 'Present Perfect Simple'
    PAST_SIMPLE_VS_PRESENT_PERFECT_SIMPLE = 'Past Simple VS Present Perfect Simple'
    PRESENT_SIMPLE_VS_PRESENT_PERFECT_SIMPLE = 'Present Simple VS Present Perfect Simple'
    PRESENT_PERFECT_SIMPLE_VS_PRESENT_PERFECT_CONT = 'Present Perfect Simple VS Present Perfect Continuous'


class ConstructionsSections(Enum):
    TO_BE_GOING_TO = 'to be going to'
    WILL_VS_BE_GOING_TO = 'will VS be going to'
    WAS_GOING_TO = 'was going to'
    THERE_ARE_THERE_IS = 'there are / there is'
    IT_TAKE = 'it take'
    USED_TO = 'used to'
    USED_TO_VS_PAST_SIMPLE = 'used to VS Past Simple'
    TAG_QUESTIONS = 'tag questions'


class PhrasesAndWordsSections(Enum):
    HOW_MUCH_HOW_MANY = 'how much how many'
    LITTLE_VS_FEW = 'little VS few'
    SOME_VS_ANY = 'some VS any'
    ENOUGH_VS_TOO = 'enough VS too'
    SO_VS_SUCH = 'so VS such'
    BECAUSE_VS_SO = 'because VS so'
    SO_VS_NEITHER = 'so VS neither'
    ARTICLES = 'articles'


class PrepositionsSections(Enum):
    PREPOSITIONS_OF_THE_TIME = 'prepositions of the time'
    PREPOSITIONS_OF_PLACE = 'prepositions of place'
    PREPOSITIONS_OF_AGENT_OR_INSTRUMENT = 'prepositions of agent or instrument'
    PREPOSITIONS_OF_CAUSE_OR_REASON = 'Prepositions of Cause or Reason:'


class ModalVerbsSections(Enum):
    CAN_VS_COULD = 'can VS could'
    CANT_VS_COULDNT = 'can’t VS couldn’t'
    MUST_VS_SHOULD = 'must VS should'
    MUST_VS_SHOULD_VS_HAVE_TO = 'must VS should VS have to'
    CAN_VS_MAY = 'can VS may'


class ConditionalsSections(Enum):
    ZERO_COND = 'zero cond'
    FIRST_COND = 'first cond'
    SECOND_COND = 'second cond'
    THIRD_COND = 'third cond'
    MIXED = 'mixed'

testing_section_mapping = {
        TestingSections.TENSES.value: TensesSections,
        TestingSections.CONSTRUCTIONS.value: ConstructionsSections,
        TestingSections.PHRASES_AND_WORDS.value: PhrasesAndWordsSections,
        TestingSections.PREPOSITIONS.value: PrepositionsSections,
        TestingSections.MODAL_VERBS.value: ModalVerbsSections,
        TestingSections.CONDITIONALS.value: ConditionalsSections,
    }


class AdminMenuButtons(Enum):
    YES = 'Да'
    NO = 'Нет'
    COMMIT = 'Отправить'
    EXERCISES = 'Тренажеры'
    CLOSE = 'Закрыть'
    MAIN_MENU = '↖️Главное меню'
    EXIT = '⬅️Выход'

    TESTING = 'Тесты'
    SET_SECTION_TESTING = 'Выбрать раздел'
    SET_SUBSECTION_TESTING = 'Выбрать тему'
    SEE_EXERCISES_TESTING = 'Посмотреть предложения'
    ADD_EXERCISE_TESTING = 'Добавить предложение'
    EDIT_EXERCISE_TESTING = 'Редактировать предложение'
    DEL_EXERCISE_TESTING = 'Удалить предложение'

    IRR_VERBS = 'Неправильные глаголы'
    SEE_VERBS = 'Посмотреть глаголы'
    ADD_VERBS = 'Добавить глагол'
    DEL_VERBS = 'Удалить глагол'

    NEW_WORDS = 'Изучение новых слов'
    SET_SECTION_NEW_WORDS = 'Выбрать раздел'
    SEE_NEW_WORDS = 'Посмотреть слова'
    ADD_NEW_WORDS = 'Добавить слово'
    DEL_NEW_WORDS = 'Удалить слово'

    SEE_ACTIVITY_DAY = 'Посмотреть активность за день'
    SEE_ACTIVITY_WEEK = 'Посмотреть активность за неделю'
    SEE_CHART = 'Посмотреть рейтинг пользователей'

    USERS = 'Пользователи'
    SEE_USERS = 'Посмотреть пользователей'
    DEL_USER = 'Удалить пользователя'

list_right_answers = [
    'You are right!', 'Awesome!', 'Great!', 'Good job',
    'You should be very proud of yourself', 'Oh, nice!', 'Fantastic!',
    'Good for you!', 'That’s really nice', 'You’re learning fast',
    'Keep up the good work', 'You’re getting better every day!', 'Excellent!',
    'Well done!', 'You’re a genius', 'Right On!',
    'Very good indeed!'
]