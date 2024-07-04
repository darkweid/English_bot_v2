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

    INFO_RULES = f"""\n🟢Весь прогресс сохраняется в памяти бота
\n🔵Регистр введенных предложений/слов не имеет значения.
\n❌Не используй сокращения «don't», «it's»
✅Используй полные формы «do not», «it is»
\n🟠В любой непонятной ситуации нажимай команду /start и бот перезапустится 😊"""
    ERROR = 'Что-то пошло не так😐\nПерезапусти бота, нажми команду /start'

    TEST_RULES = """Правила простые:\nЯ пишу предложение на английском с пробелом, а ты должен мне написать, что нужно вставить вместо этого пробела\n\nЕсли ответы не совпадут:
⚪ Можешь попробовать написать ответ ещё раз(количество попыток не ограничено)\n⚪ Можешь поcмотреть ответ, нажав на кнопку «Показать ответ»"""
    TESTING_HELLO = 'Lets get it started 💃 🕺'
    CHOOSE_SECTION = 'Выбери раздел для прохождения теста:'
    CHOOSE_SUBSECTION_TEST = 'Выбери тему для прохождения теста:'
    ALL_EXERCISES_COMPLETED = 'You’ve finished this test 💫🎉'
    INCORRECT_ANSWER = '❌ Хм, у меня другой ответ 🤔\n\n<b>Попробуй ещё раз</b> или попроси меня показать ответ 😉'
    EMPTY_SECTION = 'В этот раздел еще не добавлены упражнения 😐'
    ARE_YOU_SURE_START_AGAIN = 'Весь прогресс по этой теме будет сброшен.\nНачать проходить заново?'

    NEW_WORDS_RULES = """Я использую метод интервальных повторений\n
Слова, которые ты часто переводишь правильно, я буду показывать с каждым днём всё реже.
А те слова, которые тяжело будут запоминаться, буду показывать до тех пор, пока ты их не запомнишь.\n
Ты можешь добавить себе слова/идиомы/фразовые глаголы для изучения
и установить время напоминаний об изучении слов.\n
<b>Изучай слова каждый день, это важно при использовании интервальных
повторений</b>, и тогда прогресс не заставит себя ждать😊"""
    ABOUT_SPACED_REPETITION = """<b>Интервальные повторения</b> (на английском — Spaced Repetition) — это методика запоминания
информации, при которой повторение учебного материала происходит через увеличивающиеся интервалы времени.\n
<b><i>Основные принципы интервальных повторений:</i></b>
<b>1) Забывание и восстановление</b>: Человеческая память склонна забывать информацию с течением времени. 
Однако, если повторять информацию в нужный момент, она восстанавливается и сохраняется на более длительный срок.\n
<b>2) Оптимизация времени</b>: Методика интервальных повторений помогает сократить время, необходимое для повторения, так как фокусируется
на тех моментах, когда информация вот-вот будет забыта.\n
<b>3) Периодические пересмотры</b>: Постепенное увеличение интервалов между повторениями позволяет
информации оседать в долгосрочной памяти."""
    NEW_WORDS_HELLO = 'Lets get it started 💃 🕺'
    SELECT_SECTION_WORDS = 'Выбери раздел:'
    SELECT_SUBSECTION_WORDS = 'Выбери тему:'
    NO_WORDS_TO_LEARN_TODAY = 'На сегодня у тебя больше нет слов для изучения'

    STATS_USER = 'За какой срок нужна статистика?'
    REMINDER = 'Привет\n Не забудь сегодня позаниматься английским'
    CHOOSE_TIMEZONE = """Выбери свой часовой пояс.
Например:
Москва - UTC+3
Омск - UTC+6
Чикаго - UTC-5"""


class MainMenuButtons(Enum):
    TESTING = 'Тесты'
    IRREGULAR_VERBS = 'Изучение неправильных глаголов'
    NEW_WORDS = 'Изучение новых слов'
    TRANSLATING_SENTENCES = 'Предложения для перевода'


class BasicButtons(Enum):
    YES = '✅ Да'
    NO = '❌ Нет'
    READY = 'Готов!'
    BACK = '⬅️Назад'
    SET = 'Установить'
    CHOOSE_OTHER_SECTION = 'Выбрать другую тему'
    MAIN_MENU = '🏠Главное меню'
    MAIN_MENU_NEW_WORDS = '🏠Главное меню – Изучение слов'

    CANCEL = 'Отменить'
    CLOSE = 'Закрыть'
    RULES = '🙋‍♀️ Посмотреть правила 🙋'
    SEE_ANSWER = '🔎 Показать ответ 🔍'
    REMINDER_TIME = 'Установить время напоминаний'
    TODAY = 'Сегодня'
    LAST_WEEK = 'Последняя неделя'
    LAST_MONTH = 'Последний месяц'
    CHANGE_TIME_ZONE = 'Установить часовой пояс'
    CHANGE_REMINDER_TIME = 'Установить время напоминаний'
    TURN_OFF_REMINDER = 'Выключить напоминания'
    START_AGAIN = 'Пройти заново'

    # New Words
    LEARN_ADDED_WORDS = 'Учить добавленные слова'
    ADD_WORDS = 'Добавить слова/идиомы для изучения'
    NEW_WORDS_PROGRESS = 'Посмотреть мой прогресс в изучении слов'
    MORE_ABOUT_SPACED_REPETITION = 'Подробнее про интервальное повторение'


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


class NewWordsSections(Enum):
    WORDS_BY_TOPIC = 'Words by topic'
    IDIOMS = 'Idioms'
    PHRASAL_VERBS = 'Phrasal verbs'


class WordsByTopic(Enum):
    VEGETABLES = 'Vegetables'
    FRUITS = 'Fruits'
    CARS = 'Cars'


class Idioms(Enum):
    BUSINESS_IDIOMS = 'Business Idioms'
    FOOD_IDIOMS = 'Food Idioms'
    SPORTS_IDIOMS = 'Sports Idioms'


class PhrasalVerbs(Enum):
    TRAVEL_PHRASAL_VERBS = 'Travel Phrasal Verbs'
    WORK_PHRASAL_VERBS = 'Work Phrasal Verbs'
    RELATIONSHIP_PHRASAL_VERBS = 'Relationship Phrasal Verbs'


new_words_section_mapping = {
    NewWordsSections.WORDS_BY_TOPIC.value: WordsByTopic,
    NewWordsSections.IDIOMS.value: Idioms,
    NewWordsSections.PHRASAL_VERBS.value: PhrasalVerbs
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
    SEE_NEW_WORDS = 'Посмотреть слова/идиомы'
    ADD_NEW_WORDS = 'Добавить слова/идиомы'
    EDIT_NEW_WORDS = 'Изменить слово/идиому'
    DEL_NEW_WORDS = 'Удалить слово/идиому'

    SEE_ACTIVITY_DAY = 'Посмотреть активность за день'
    SEE_ACTIVITY_WEEK = 'Посмотреть активность за неделю'
    SEE_ACTIVITY_MONTH = 'Посмотреть активность за месяц'

    USERS = 'Пользователи'
    DEL_USER = 'Удалить пользователя'
    ADD_WORDS_TO_USER_LEARNING = 'Добавить пользователю слова'

    BROADCAST = 'Рассылка пользователям'
    DEL_BROADCASTS = 'Удалить все запланированные рассылки'
    ADD_BROADCAST = 'Запланировать рассылку'


list_right_answers = [
    'You are right!', 'Awesome!', 'Great!', 'Good job',
    'You should be very proud of yourself', 'Oh, nice!', 'Fantastic!',
    'Good for you!', 'That’s really nice', 'You’re learning fast',
    'Keep up the good work', 'You’re getting better every day!', 'Excellent!',
    'Well done!', 'You’re a genius', 'Right On!',
    'Very good indeed!'
]
