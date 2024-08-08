from datetime import date
from sqlalchemy import Column, Integer, String, Date, DateTime, Time, ForeignKey, Boolean, Index, ForeignKeyConstraint
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


class NewWords(Base):
    __tablename__ = 'new_words'
    section = Column(String, primary_key=True, nullable=False)
    subsection = Column(String, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    russian = Column(String, nullable=False)
    english = Column(String, nullable=False)
    user_words = relationship("UserWordsLearning", back_populates="new_word")


class UserWordsLearning(Base):
    __tablename__ = 'user_words_learning'
    user_id = Column(Integer, primary_key=True, nullable=False, index=True)
    section = Column(String, primary_key=True, nullable=False, index=True)
    subsection = Column(String, primary_key=True, nullable=False, index=True)
    exercise_id = Column(Integer, primary_key=True, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    success = Column(Integer, default=0, nullable=False)
    level_SR = Column(Integer, default=0, nullable=False)
    next_review_date = Column(Date, default=date.today(), nullable=False)
    date = Column(Date, default=date.today(), nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(
            ['section', 'subsection', 'exercise_id'],
            ['new_words.section', 'new_words.subsection', 'new_words.id']
        ),
    )

    new_word = relationship("NewWords", back_populates="user_words")


Index('ix_user_section', UserWordsLearning.user_id, UserWordsLearning.section,
      UserWordsLearning.subsection)


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


class DailyStatistics(Base):
    __tablename__ = 'daily_statistics'
    date = Column(Date, primary_key=True, nullable=False)
    total_testing_exercises = Column(Integer, default=0, nullable=False)
    total_new_words = Column(Integer, default=0, nullable=False)
    total_irregular_verbs = Column(Integer, default=0, nullable=False)
    new_users = Column(Integer, default=0, nullable=False)


Index('ix_daily_statistics_date', DailyStatistics.date)
