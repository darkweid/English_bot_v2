from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import func
from db.models import Base, TestingExercise, IrregularVerb, NewWord, UserProgress, User
from db.init import engine
from datetime import datetime

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
            res = await session.execute(select(TestingExercise).filter_by(subsection=subsection).order_by(TestingExercise.id))
            exercises = res.scalars().all()
            result = ''
            for exercise in exercises:
                result += f'{exercise.id}) {exercise.test}. Ответ: {exercise.answer}\n\n'
            return result

    async def get_irregular_verbs(self):
        async with self.db as session:
            result = await session.execute(select(IrregularVerb))
            return result.scalars().all()

    async def get_new_words(self):
        async with self.db as session:
            result = await session.execute(select(NewWord))
            return result.scalars().all()


class UserProgressManager(DatabaseManager):
    async def init_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def mark_exercise_completed(self, user_id, exercise_type, exercise_section, exercise_id, success):
        async with self.db as session:
            async with session.begin():
                progress = await session.get(
                    UserProgress, (user_id, exercise_type, exercise_section, exercise_id)
                )
                if progress:
                    if not success:
                        progress.attempts += 1
                else:
                    progress = UserProgress(
                        user_id=user_id,
                        exercise_type=exercise_type,
                        exercise_section=exercise_section,
                        exercise_id=exercise_id,
                        attempts=1,
                        date=datetime.utcnow().date(),

                    )
                session.add(progress)

    async def get_completed_exercises(self, user_id, exercise_type):
        async with self.db as session:
            result = await session.execute(
                select(UserProgress).where(
                    UserProgress.user_id == user_id,
                    UserProgress.exercise_type == exercise_type
                )
            )
            return [row.exercise_id for row in result.scalars().all()]


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
