from time import strftime
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import func, update, delete, not_, desc
from db.models import Base, TestingExercise, IrregularVerb, NewWord, UserProgress, User
from db.init import engine
from datetime import datetime, date, timedelta
import random

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseManager:
    def __init__(self):
        self.db = SessionLocal()

    async def close(self):
        await self.db.close()


class ExerciseManager(DatabaseManager):
    async def init_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_testing_exercise(self, section, subsection, test, answer):
        async with self.db as session:
            async with session.begin():
                # Найти максимальный ID для данного раздела
                max_id = await session.execute(
                    select(func.max(TestingExercise.id)).filter_by(section=section, subsection=subsection))
                max_id = max_id.scalar() or 0
                next_id = max_id + 1

                exercise = TestingExercise(section=section, subsection=subsection, id=next_id, test=test, answer=answer)
                session.add(exercise)

    async def add_irregular_verb(self, russian, english):
        async with self.db as session:
            async with session.begin():
                verb = IrregularVerb(russian=russian, english=english)
                session.add(verb)

    async def add_new_word(self, section, russian, english):
        async with self.db as session:
            async with session.begin():
                # Найти максимальный ID для данного раздела
                max_id = await session.execute(select(func.max(NewWord.id)).filter_by(section=section))
                max_id = max_id.scalar() or 0
                next_id = max_id + 1

                word = NewWord(section=section, id=next_id, russian=russian, english=english)
                session.add(word)

    async def get_testing_exercises(self, subsection: str):
        async with self.db as session:
            res = await session.execute(
                select(TestingExercise).filter_by(subsection=subsection).order_by(TestingExercise.id))
            exercises = res.scalars().all()
            result = ''
            for exercise in exercises:
                result += f'{exercise.id}) {exercise.test}. Ответ: {exercise.answer}\n\n'
            return result

    async def get_random_testing_exercise(self, section: str, subsection: str, user_id: int):
        async with self.db as session:
            # Подзапрос для получения ID упражнений, которые пользователь уже выполнил успешно
            subquery = (select(UserProgress.exercise_id).filter(
                UserProgress.user_id == user_id,
                UserProgress.exercise_section == section,
                UserProgress.exercise_subsection == subsection,
                UserProgress.success == True)).subquery()

            # Основной запрос для получения упражнений, которые пользователь еще не выполнял успешно
            stmt = (
                select(TestingExercise)
                .filter(
                    TestingExercise.section == section,
                    TestingExercise.subsection == subsection,
                    TestingExercise.id.not_in(subquery)
                )
            )

            result = await session.execute(stmt)
            exercises = result.scalars().all()

            if not exercises:
                return None  # Если нет доступных упражнений
            result = random.choice(exercises)
            # Возвращаем случайное упражнение из списка
            return (result.test, result.answer, result.id)

    async def get_irregular_verbs(self):
        async with self.db as session:
            result = await session.execute(select(IrregularVerb))
            return result.scalars().all()

    async def get_new_words(self):
        async with self.db as session:
            result = await session.execute(select(NewWord))
            return result.scalars().all()

    async def edit_testing_exercise(self, section, subsection, test, answer, index):
        async with self.db as session:
            async with session.begin():
                await session.execute(
                    update(TestingExercise).where(TestingExercise.section == section,
                                                  TestingExercise.subsection == subsection,
                                                  TestingExercise.id == index).values(test=test, answer=answer))

    async def delete_testing_exercise(self, section, subsection, index):
        async with self.db as session:
            async with session.begin():
                await session.execute(
                    delete(TestingExercise).where(TestingExercise.section == section,
                                                  TestingExercise.subsection == subsection,
                                                  TestingExercise.id == index))


class UserProgressManager(DatabaseManager):
    async def init_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def mark_exercise_completed(self, user_id, exercise_type, subsection, section, exercise_id,
                                      success):
        async with self.db as session:
            first_try = False
            stmt = (
                update(UserProgress)
                .where(
                    UserProgress.user_id == user_id,
                    UserProgress.exercise_type == exercise_type,
                    UserProgress.exercise_section == section,
                    UserProgress.exercise_subsection == subsection,
                    UserProgress.exercise_id == exercise_id
                )
                .values(
                    attempts=UserProgress.attempts + 1,
                    success=success,
                    date=date.today()
                )
            )
            result = await session.execute(stmt)

            points = (1 if success else -1)
            stmt = (update(User).where(User.user_id == user_id).values(points=User.points + points))
            await session.execute(stmt)

            if result.rowcount == 0:
                new_record = UserProgress(
                    user_id=user_id,
                    exercise_type=exercise_type,
                    exercise_section=section,
                    exercise_subsection=subsection,
                    exercise_id=exercise_id,
                    attempts=1,
                    success=success,
                    date=date.today()
                )
                session.add(new_record)
                first_try = True

            await session.commit()
            return first_try

    async def get_completed_exercises_testing(self, user_id, section, subsection):
        async with self.db as session:
            # Выполнение запроса для получения количества успешных упражнений
            success_exercises_result = await session.execute(
                select(func.count()).select_from(UserProgress).where(
                    UserProgress.user_id == user_id,
                    UserProgress.exercise_type == 'Testing',
                    UserProgress.exercise_section == section,
                    UserProgress.exercise_subsection == subsection,
                    UserProgress.success == True
                )
            )
            success_exercises_count = success_exercises_result.scalar()

            exercises_result = await session.execute(
                select(func.count()).select_from(TestingExercise).where(
                    TestingExercise.section == section,
                    TestingExercise.subsection == subsection
                )
            )
            exercises_count = exercises_result.scalar()

            # Вывод результатов
            print(f'\n\n\nSuccess exercises: {success_exercises_count}, Total exercises: {exercises_count}\n')
            print(f'All exercises completed: {success_exercises_count == exercises_count}\n\n')

            return success_exercises_count == exercises_count

    async def get_activity(self, interval: int = 0):
        async with self.db as session:
            target_date = (datetime.utcnow() - timedelta(days=interval)).date()
            now = datetime.utcnow().date()
            result_testing = (await session.execute(
                select(func.count()).select_from(UserProgress).where(
                    UserProgress.exercise_type == 'Testing',
                    UserProgress.date >= target_date,
                    UserProgress.date <= now))).scalar()

            result_new_words = (await session.execute(
                select(func.count()).select_from(UserProgress).where(
                    UserProgress.exercise_type == 'New words',
                    UserProgress.date >= target_date,
                    UserProgress.date <= now))).scalar()

            result_irregular_verbs = (await session.execute(
                select(func.count()).select_from(UserProgress).where(
                    UserProgress.exercise_type == 'Irregular verbs',
                    UserProgress.date >= target_date,
                    func.date(UserProgress.date) <= now))).scalar()
            result_new_users = (await session.execute(
                select(func.count()).select_from(User).where(
                    func.date(User.registration_date) >= target_date,
                    func.date(User.registration_date) <= now))).scalar()

            if interval == 0:
                text = 'сегодня'
            elif interval == 7:
                text = 'последнюю неделю'
            elif interval == 30:
                text = 'последний месяц'
            info = f"""Статистика по всем пользователям за {text}:
Тестирование: {result_testing}
Изучение новых слов: {result_new_words}
Неправильные глаголы: {result_irregular_verbs}
Новых пользователей: {result_new_users}"""

            return info

    async def get_activity_by_user(self, user_id: int, interval: int = 0):
        async with self.db as session:
            target_date = (datetime.utcnow() - timedelta(days=interval)).date()
            now = datetime.utcnow().date()
            result_testing = (await session.execute(
                select(func.count()).select_from(UserProgress).where(
                    UserProgress.exercise_type == 'Testing',
                    UserProgress.date >= target_date,
                    UserProgress.date <= now,
                    UserProgress.user_id == user_id))).scalar()

            result_new_words = (await session.execute(
                select(func.count()).select_from(UserProgress).where(
                    UserProgress.exercise_type == 'New words',
                    UserProgress.date >= target_date,
                    UserProgress.date <= now,
                    UserProgress.user_id == user_id))).scalar()

            result_irregular_verbs = (await session.execute(
                select(func.count()).select_from(UserProgress).where(
                    UserProgress.exercise_type == 'Irregular verbs',
                    UserProgress.date >= target_date,
                    func.date(UserProgress.date) <= now,
                    UserProgress.user_id == user_id))).scalar()
            if interval == 0:
                text = 'сегодня'
            elif interval == 7:
                text = 'последнюю неделю'
            elif interval == 30:
                text = 'последний месяц'
            info = f"""
Твоя статистика за <b>{text}</b>:
Тестирование: {result_testing}
Изучение новых слов: {result_new_words}
Неправильные глаголы: {result_irregular_verbs}
"""

            return info

    async def get_user_points(self, user_id: int):
        async with self.db as session:
            result_points = (await session.execute(
                select(User.points).select_from(User).where(
                    User.user_id == user_id))).scalar()

            return result_points

    async def get_user_rank_and_total(self, user_id: int, medals_rank: bool = False):
        async with self.db as session:
            async with session.begin():
                user_points = (await session.execute(
                    select(User.points).where(User.user_id == user_id))).scalar()

                higher_ranked_count = (await session.execute(
                    select(func.count()).select_from(User).where(User.points > user_points)
                )).scalar()

                total_users = (await session.execute(
                    select(func.count()).select_from(User)
                )).scalar()
                user_rank = higher_ranked_count + 1
                if medals_rank:
                    if user_rank == 1:
                        user_rank = '🥇'
                    elif user_rank == 2:
                        user_rank = '🥈'
                    elif user_rank == 3:
                        user_rank = '🥉'

                return user_rank, total_users

    async def get_all_users_ranks_and_points(self, medals_rank: bool = False):
        async with self.db as session:
            async with session.begin():
                users = await session.execute(
                    select(User.id, User.user_id, User.full_name, User.tg_login, User.points)
                    .order_by(desc(User.points))
                )

                users = users.fetchall()

                users_with_ranks = []

                for rank, user in enumerate(users, start=1):
                    if medals_rank:
                        if rank == 1:
                            rank = '🥇'
                        elif rank == 2:
                            rank = '🥈'
                        elif rank == 3:
                            rank = '🥉'

                    users_with_ranks.append({
                        'rank': str(rank),
                        'user_id': str(user.user_id),
                        'full_name': user.full_name,
                        'tg_login': user.tg_login,
                        'points': str(user.points)
                    })

                return users_with_ranks


class UserManager(DatabaseManager):
    async def init_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, user_id, full_name, tg_login):
        async with self.db as session:
            async with session.begin():
                # Проверка на существование пользователя
                result = await session.execute(select(User).filter_by(user_id=user_id))
                existing_user = result.scalar_one_or_none()
                if existing_user:
                    print(f"User with user_id {user_id}:{full_name} already exists.")
                    return None

                user = User(
                    registration_date=datetime.utcnow(),
                    user_id=user_id,
                    full_name=full_name,
                    tg_login=tg_login,
                    reminder_time=None,
                    time_zone=None
                )
                session.add(user)
                await session.commit()
                print(f"User {full_name} added successfully.")
                return None

    async def get_all_users(self):
        async with self.db as session:
            async with session.begin():
                result = await session.execute(select(User))
                users = result.scalars().all()  # Извлекаем все строки как объекты User

                # Создаем список словарей с информацией о каждом пользователе
                user_info = [
                    {
                        'id': user.id,
                        'user_id': user.user_id,
                        'full_name': user.full_name,
                        'tg_login': user.tg_login,
                        'registration_date': user.registration_date,
                        'points': user.points,
                        'reminder_time': user.reminder_time,
                        'time_zone': user.time_zone
                    }
                    for user in users
                ]

                return user_info

    async def get_user_info(self, user_id: int, admin: bool = True):
        async with self.db as session:
            async with session.begin():
                result = await session.execute(select(User).filter_by(user_id=user_id))
                user = result.scalars().first()
                if user:
                    info = ''
                    if admin:
                        info += f"""Имя: {user.full_name}
telegram: @{user.tg_login}
telegram id: {user.user_id}
Баллов: {user.points}\n"""

                    info += f"""Дата регистрации: {user.registration_date.strftime('%d-%m-%Y | %H:%M UTC')}
Время напоминаний: { user.reminder_time if user.reminder_time else 'Не установлено'}
Часовой пояс: {user.time_zone if user.time_zone else 'Не установлен'}"""

                    return info
                return None
