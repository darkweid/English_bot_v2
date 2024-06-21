from sqlalchemy import Column, Integer, String, Date, DateTime, Time, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TestingExercise(Base):
    __tablename__ = 'testing_exercises'
    section = Column(String, primary_key=True, nullable=False)
    subsection = Column(String, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    test = Column(String, nullable=False)
    answer = Column(String, nullable=False)


class IrregularVerb(Base):
    __tablename__ = 'irregular_verbs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    russian = Column(String, nullable=False)
    english = Column(String, nullable=False)


class NewWord(Base):
    __tablename__ = 'new_words'
    section = Column(String, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    russian = Column(String, nullable=False)
    english = Column(String, nullable=False)


class UserProgress(Base):
    __tablename__ = 'user_progress'
    user_id = Column(Integer, primary_key=True, nullable=False)
    exercise_type = Column(String, primary_key=True, nullable=False)
    exercise_section = Column(Integer, primary_key=True, nullable=True)
    exercise_subsection = Column(Integer, primary_key=True, nullable=True)
    exercise_id = Column(Integer, primary_key=True, nullable=False)
    attempts = Column(Integer, default=1)
    success = Column(Boolean, default=False)
    date = Column(Date, nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_date = Column(DateTime)
    user_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String)
    tg_login = Column(String)
    points = Column(Integer, default=0)
    reminder_time = Column(Time)
    time_zone = Column(String)
