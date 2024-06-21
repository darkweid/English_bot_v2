from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import func, update, delete, not_
from db.models import Base, TestingExercise, IrregularVerb, NewWord, UserProgress, User
from db.init import engine
from datetime import datetime, date
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


    async def get_completed_exercises(self, user_id, exercise_type, section, subsection):
        async with self.db as session:
            result = await session.execute(
                select(func.count()).select_from(UserProgress).where(
                    UserProgress.user_id == user_id,
                    UserProgress.exercise_type == exercise_type
                )
            )


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
