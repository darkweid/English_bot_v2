from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Time
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class GrammarExercise(Base):
    __tablename__ = 'grammar_exercises'
    section = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    russian = Column(String, nullable=False)
    english = Column(String, nullable=False)


class IrregularVerb(Base):
    __tablename__ = 'irregular_verbs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    russian = Column(String, nullable=False)
    english = Column(String, nullable=False)


class NewWord(Base):
    __tablename__ = 'new_words'
    section_id = Column(Integer, nullable=False)
    section_name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    russian = Column(String, nullable=False)
    english = Column(String, nullable=False)


class UserProgress(Base):
    __tablename__ = 'user_progress'
    user_id = Column(Integer, primary_key=True)
    exercise_type = Column(String, primary_key=True)
    exercise_section = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_date = Column(DateTime)
    user_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String)
    tg_login = Column(String)
    grammar_current_level = Column(Integer)
    points = Column(Integer, default=0)
    reminder_time = Column(Time)
    time_zone = Column(String)
