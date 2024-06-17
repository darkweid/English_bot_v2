from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from db.models import Base, GrammarExercise, IrregularVerb, NewWord, UserProgress, User
from db.init import engine
from datetime import datetime

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


class DatabaseManager:
    def __init__(self):
        self.db = SessionLocal()

    async def close(self):
        await self.db.close()


class ExerciseManager(DatabaseManager):
    async def init_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_grammar_exercise(self, russian, english, level):
        async with self.db as session:
            async with session.begin():
                exercise = GrammarExercise(russian=russian, english=english, level=level)
                session.add(exercise)

    async def add_irregular_verb(self, russian, english, level):
        async with self.db as session:
            async with session.begin():
                verb = IrregularVerb(russian=russian, english=english, level=level)
                session.add(verb)

    async def add_new_word(self, russian, english, level):
        async with self.db as session:
            async with session.begin():
                word = NewWord(russian=russian, english=english, level=level)
                session.add(word)

    async def get_grammar_exercises(self):
        async with self.db as session:
            result = await session.execute(select(GrammarExercise))
            return result.scalars().all()

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

    async def mark_exercise_completed(self, user_id, exercise_type, exercise_id):
        async with self.db as session:
            async with session.begin():
                progress = UserProgress(user_id=user_id, exercise_type=exercise_type, exercise_id=exercise_id)
                session.add(progress)

    async def get_completed_exercises(self, user_id, exercise_type):
        async with self.db as session:
            result = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id,
                                                                      UserProgress.exercise_type == exercise_type))
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
                    grammar_current_level=1,
                    reminder_time=None,
                    time_zone=None
                )
                session.add(user)
                await session.commit()
                return f"User {full_name} added successfully."
