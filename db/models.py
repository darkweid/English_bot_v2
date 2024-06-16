import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Time
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class GrammarExercise(Base):
    __tablename__ = 'grammar_exercises'
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    russian = Column(String, nullable=False)
    english = Column(String, nullable=False)
    level = Column(Integer, nullable=False)


class UserProgress(Base):
    __tablename__ = 'user_progress'
    user_id = Column(Integer, primary_key=True)
    exercise_type = Column(String, primary_key=True)
    exercise_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True)
    registration_date = Column(DateTime)
    user_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    tg_login = Column(String)
    grammar_current_level = Column(Integer)
    reminder_time = Column(Time)
    time_zone = Column(String)
